import logging
import pathlib
from logging import Logger
from pathlib import Path
from typing import Callable, List, Optional

from verified_cogen.args import ProgramArgs, get_args
from verified_cogen.llm import LLM
from verified_cogen.runners import Runner, RunnerConfig
from verified_cogen.runners.flush import FlushRunner
from verified_cogen.runners.generate import GenerateRunner
from verified_cogen.runners.generic import GenericRunner
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType, LanguageDatabase
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.runners.rewriters.nagini_rewriter import NaginiRewriter
from verified_cogen.runners.rewriters.nagini_rewriter_fixing import NaginiRewriterFixing
from verified_cogen.runners.rewriters.nagini_rewriter_fixing_ast import (
    NaginiRewriterFixingAST,
)
from verified_cogen.runners.step_by_step import StepByStepRunner
from verified_cogen.runners.validating import ValidatingRunner, Validator
from verified_cogen.tools import (
    ext_glob,
    extension_from_file_list,
    get_cache_dir,
    pprint_stat,
    register_output_handler,
    rename_file,
    tabulate_list,
)
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

logger = logging.getLogger(__name__)


def run_once(
    files: list[Path],
    args: ProgramArgs,
    runner_cls: Callable[[LLM, Logger, Verifier, Optional[Rewriter]], Runner],
    verifier: Verifier,
    mode: Mode,
    rewriter: Optional[Rewriter],
    is_once: bool,
) -> tuple[int, int, int, dict[str, int]]:
    _init: tuple[list[str], list[str], list[str]] = ([], [], [])
    success, success_zero_tries, failed = _init

    cnt: dict[str, int] = dict()

    for file in files:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )

        runner = runner_cls(llm, logger, verifier, rewriter)

        retries = args.retries + 1
        tries = None
        while retries > 0 and tries is None:
            tries = runner.run_on_file(mode, args.tries, str(file))
            retries -= 1

        name = rename_file(file)
        if tries == 0:
            logger.info(f"{name} verified without modification")
            success_zero_tries.append(name)
        elif tries is not None:
            logger.info(f"{name} verified with modification")
            success.append(name)
        else:
            logger.error(f"{name} failed")
            failed.append(name)

        if tries is not None:
            cnt[name] = tries

        llm.dump_history(Path(get_cache_dir()) / "history" / f"{name}.txt")

    if is_once:
        if args.output_style == "full":
            success_zero_tries_tabbed = tabulate_list(success_zero_tries)
            success_tabbed = tabulate_list(success)
            failed_tabbed = tabulate_list(failed)
            if len(success_zero_tries) > 0:
                print(f"Verified without modification: {success_zero_tries_tabbed}")
            if len(success) > 0:
                print(f"Verified with modification: {success_tabbed}")
            if len(failed) > 0:
                print(f"Failed: {failed_tabbed}")

        pprint_stat("Verified without modification", len(success_zero_tries), len(files))
        pprint_stat("Verified with modification", len(success), len(files))
        pprint_stat("Failed", len(failed), len(files))

    return len(success_zero_tries), len(success), len(failed), cnt


def construct_nagini_rewriter(runner_types: List[str]) -> Optional[Rewriter]:
    runner = None
    for runner_type in runner_types:
        if runner_type == "NaginiRewriter":
            runner = NaginiRewriter()
        elif runner_type == "NaginiRewriterFixing":
            runner = NaginiRewriterFixing(runner)
        elif runner_type == "NaginiRewriterFixingAST":
            runner = NaginiRewriterFixingAST(runner)
        else:
            raise ValueError(f"Unexpected nagini rewriter type: {runner_type}")
    return runner


def construct_rewriter(extension: str, runner_types: List[str]) -> Optional[Rewriter]:
    if extension == "py":
        return construct_nagini_rewriter(runner_types)
    if runner_types:
        raise ValueError(f"Not implemented rewriters for language: {LanguageDatabase().regularise[extension]}")
    return None


def make_runner_cls(
    bench_type: str, extension: str, config: RunnerConfig
) -> Callable[[LLM, Logger, Verifier, Optional[Rewriter]], Runner]:
    def runner_cls(
        llm: LLM,
        logger: Logger,
        verifier: Verifier,
        rewriter: Optional[Rewriter] = None,
        validator: Optional[Validator] = None,
    ):
        if bench_type == "invariants":
            return InvariantRunner(llm, logger, verifier, config)
        elif bench_type == "generic":
            return GenericRunner(llm, logger, verifier, config)
        elif bench_type == "generate":
            return GenerateRunner(llm, logger, verifier, config)
        elif bench_type == "validating":
            return ValidatingRunner(
                InvariantRunner(llm, logger, verifier, config, rewriter),
                LanguageDatabase().get(extension),
                validator,
            )
        elif bench_type == "step-by-step":
            return ValidatingRunner(
                StepByStepRunner(InvariantRunner(llm, logger, verifier, config, rewriter)),
                LanguageDatabase().get(extension),
            )
        elif bench_type == "step-by-step-flush":
            return ValidatingRunner(
                FlushRunner(StepByStepRunner(InvariantRunner(llm, logger, verifier, config, rewriter))),
                LanguageDatabase().get(extension),
            )
        else:
            raise ValueError(f"Unexpected bench_type: {bench_type}")

    return runner_cls


def main():
    args = get_args()
    all_removed = [AnnotationType.INVARIANTS, AnnotationType.ASSERTS]
    if args.remove_conditions:
        all_removed += [AnnotationType.PRE_CONDITIONS, AnnotationType.POST_CONDITIONS]
    if args.remove_implementations:
        all_removed += [AnnotationType.IMPLS]
    if args.remove_pure:
        all_removed += [AnnotationType.PURE]

    register_basic_languages(with_removed=all_removed)
    mode = Mode(args.insert_conditions_mode)
    if mode == Mode.REGEX:
        if "dafny" not in args.verifier_command:
            raise ValueError("Regex mode only works with Dafny verifier")

        if args.bench_type == "generic":
            raise ValueError("Regex mode only works with invariants")

    if args.output_logging:
        register_output_handler(logger)

    if args.input is None and args.dir is None:
        args.input = input("Input file: ").strip()
    log_tries = pathlib.Path(args.log_tries) if args.log_tries is not None else None

    verifier = Verifier(args.verifier_command, args.verifier_timeout)
    config = RunnerConfig(
        log_tries=log_tries,
        include_text_descriptions=args.include_text_descriptions,
        remove_implementations=args.remove_implementations,
        remove_helpers=args.remove_pure,
    )
    if args.dir is not None:
        files = sorted(list(pathlib.Path(args.dir).glob(ext_glob(args.filter_by_ext))))
        runner_cls = make_runner_cls(args.bench_type, extension_from_file_list(files), config)
        rewriter = construct_rewriter(extension_from_file_list(files), args.manual_rewriters)
        runner = runner_cls(
            LLM(
                args.grazie_token,
                args.llm_profile,
                args.prompts_directory,
                args.temperature,
            ),
            logger,
            verifier,
            rewriter,
        )
        for file in files:
            with open(file) as f:
                runner.precheck(f.read(), mode)

        if args.runs == 1:
            _, _, _, total_cnt = run_once(files, args, runner_cls, verifier, mode, rewriter, is_once=True)
        else:
            success_zero_tries, success, failed = 0, 0, 0
            total_cnt = {rename_file(f): 0 for f in files}
            for _ in range(args.runs):
                s0, s, f, cnt = run_once(files, args, runner_cls, verifier, mode, rewriter, is_once=False)
                success_zero_tries += s0
                success += s
                failed += f

                new_total: dict[str, int] = dict()
                for k in set(cnt.keys()) & set(total_cnt.keys()):
                    new_total[k] = cnt[k] + total_cnt[k]
                total_cnt = new_total

            pprint_stat(
                "Verified without modification",
                success_zero_tries,
                len(files),
                args.runs,
            )
            pprint_stat("Verified with modification", success, len(files), args.runs)
            pprint_stat("Failed", failed, len(files), args.runs)

        with open(pathlib.Path(get_cache_dir()) / "total_cnt.json", "w") as f:
            import json

            json.dump({k: v / args.runs for k, v in total_cnt.items()}, f)
    else:
        assert args.input is not None, "input file must be specified"
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )
        runner = make_runner_cls(args.bench_type, Path(args.input).suffix[1:], config)(llm, logger, verifier, None)
        tries = runner.run_on_file(mode, args.tries, args.input)
        if tries == 0:
            print("Verified without modification")
        elif tries is not None:
            print("Verified with modification on try", tries)
        else:
            print("Failed to verify")

        llm.dump_history(Path("dump.txt"))
