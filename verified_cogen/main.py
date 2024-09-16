import logging
import pathlib

from verified_cogen.args import get_args
from verified_cogen.llm import LLM
from verified_cogen.runners.generate import GenerateRunner
from verified_cogen.runners.generic import GenericRunner
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.validating import ValidatingRunner
from verified_cogen.tools import (
    ext_glob,
    pprint_stat,
    rename_file,
    tabulate_list,
    extension_from_file_list,
)
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier
from pathlib import Path
from typing import Callable, Optional
from verified_cogen.runners import Runner
from logging import Logger

logger = logging.getLogger(__name__)


def run_once(
    files: list[Path],
    args,
    runner_cls: Callable[[LLM, Logger, Verifier], Runner],
    verifier: Verifier,
    mode: Mode,
    is_once: bool,
) -> tuple[int, int, int]:
    success, success_zero_tries, failed = [], [], []

    for file in files:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )

        runner = runner_cls(llm, logger, verifier)

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

        pprint_stat(
            "Verified without modification", len(success_zero_tries), len(files)
        )
        pprint_stat("Verified with modification", len(success), len(files))
        pprint_stat("Failed", len(failed), len(files))

    return len(success_zero_tries), len(success), len(failed)


def make_runner_cls(
    bench_type: str, extension: str, log_tries: Optional[pathlib.Path]
) -> Callable[[LLM, Logger, Verifier], Runner]:
    def runner_cls(llm: LLM, logger: Logger, verifier: Verifier):
        match bench_type:
            case "invariants":
                return InvariantRunner(llm, logger, verifier, log_tries)
            case "generic":
                return GenericRunner(llm, logger, verifier, log_tries)
            case "generate":
                return GenerateRunner(llm, logger, verifier, log_tries)
            case "validating":
                return ValidatingRunner(
                    InvariantRunner(llm, logger, verifier, log_tries),
                    LanguageDatabase().get(extension),
                )
            case _:
                raise ValueError(f"Unexpected bench_type: {bench_type}")

    return runner_cls


def main():
    register_basic_languages()

    args = get_args()
    mode = Mode(args.insert_conditions_mode)
    if mode == Mode.REGEX:
        if "dafny" not in args.verifier_command:
            raise ValueError("Regex mode only works with Dafny verifier")

        if args.bench_type == "generic":
            raise ValueError("Regex mode only works with invariants")

    if args.input is None and args.dir is None:
        args.input = input("Input file: ").strip()
    log_tries = pathlib.Path(args.log_tries) if args.log_tries is not None else None

    verifier = Verifier(args.shell, args.verifier_command, args.verifier_timeout)
    if args.dir is not None:
        files = sorted(list(pathlib.Path(args.dir).glob(ext_glob(args.filter_by_ext))))
        runner_cls = make_runner_cls(
            args.bench_type, extension_from_file_list(files), log_tries
        )
        runner = runner_cls(
            LLM(
                args.grazie_token,
                args.llm_profile,
                args.prompts_directory,
                args.temperature,
            ),
            logger,
            verifier,
        )
        for file in files:
            with open(file) as f:
                runner.precheck(f.read(), mode)

        if args.runs == 1:
            run_once(files, args, runner_cls, verifier, mode, is_once=True)
        else:
            success_zero_tries, success, failed = 0, 0, 0
            for _ in range(args.runs):
                s0, s, f = run_once(
                    files, args, runner_cls, verifier, mode, is_once=False
                )
                success_zero_tries += s0
                success += s
                failed += f

            pprint_stat(
                "Verified without modification",
                success_zero_tries,
                len(files),
                args.runs,
            )
            pprint_stat("Verified with modification", success, len(files), args.runs)
            pprint_stat("Failed", failed, len(files), args.runs)
    else:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )
        runner = make_runner_cls(
            args.bench_type, Path(args.input).suffix[1:], log_tries
        )(llm, logger, verifier)
        tries = runner.run_on_file(mode, args.tries, args.input)
        if tries == 0:
            print("Verified without modification")
        elif tries is not None:
            print("Verified with modification on try", tries)
        else:
            print("Failed to verify")
