import json
import logging
import pathlib
from typing import no_type_check

from verified_cogen.args import ProgramArgs, get_default_parser
from verified_cogen.llm.llm import LLM
from verified_cogen.main import make_runner_cls, construct_rewriter
from verified_cogen.runners import RunnerConfig
from verified_cogen.runners.languages import AnnotationType, register_basic_languages
from verified_cogen.tools import (
    ext_glob,
    extension_from_file_list,
    register_output_handler,
    rename_file,
)
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier


class IncrementalRunArgs(ProgramArgs):
    ignore_failed: bool

    @no_type_check
    def __init__(self, args):
        super().__init__(args)
        self.ignore_failed = args.ignore_failed


logger = logging.getLogger(__name__)


def main():
    parser = get_default_parser()
    parser.add_argument(
        "--ignore-failed", help="Ignore failed files", action="store_true"
    )
    args = IncrementalRunArgs(parser.parse_args())
    print(args.manual_rewriters)

    all_removed = [AnnotationType.INVARIANTS, AnnotationType.ASSERTS]
    if args.remove_conditions:
        all_removed += [AnnotationType.PRE_CONDITIONS, AnnotationType.POST_CONDITIONS]
    if args.remove_implementations:
        all_removed += [AnnotationType.IMPLS]

    register_basic_languages(with_removed=all_removed)

    mode = Mode(args.insert_conditions_mode)
    assert mode != Mode.REGEX
    assert args.dir is not None
    assert args.runs == 1
    assert args.retries == 0

    if args.output_logging:
        register_output_handler(logger)

    directory = pathlib.Path(args.dir)
    history_dir = pathlib.Path("results") / f"history_{directory.name}"
    history_dir.mkdir(exist_ok=True)
    log_tries = pathlib.Path(args.log_tries) if args.log_tries is not None else None
    results_directory = pathlib.Path("results")
    results_directory.mkdir(exist_ok=True)
    json_results = pathlib.Path("results") / f"tries_{directory.name}.json"
    if not json_results.exists():
        with open(json_results, "w") as f:
            json.dump({}, f)
    with open(json_results, "r") as f:
        results = json.load(f)

    files = list(directory.glob(ext_glob(args.filter_by_ext)))
    assert len(files) > 0, "No files found in the directory"
    files.sort()

    verifier = Verifier(args.verifier_command)

    config = RunnerConfig(
        log_tries=log_tries,
        include_text_descriptions=args.include_text_descriptions,
        remove_implementations=args.remove_implementations,
    )
    for file in files:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )
        rewriter = construct_rewriter(
            extension_from_file_list([file]), args.manual_rewriters
        )
        runner = make_runner_cls(
            args.bench_type, extension_from_file_list([file]), config
        )(llm, logger, verifier, rewriter)
        display_name = rename_file(file)
        marker_name = str(file.relative_to(directory))
        if (
            marker_name in results
            and isinstance(results[marker_name], int)
            and results[marker_name] != -1
        ):
            logger.info(f"Skipping: {display_name} as it has already been verified")
            continue
        elif (
            marker_name in results and results[marker_name] == -1 and args.ignore_failed
        ):
            logger.info(
                f"Skipping: {display_name} as it failed previously and ignore_failed is set"
            )
            continue
        logger.info(f"Processing: {display_name}")
        try:
            tries = runner.run_on_file(mode, args.tries, str(file))
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)
            tries = None
        if tries is not None:
            results[marker_name] = tries
            logger.info(f"Verified {display_name} in {tries} tries")
        else:
            results[marker_name] = -1
            logger.info(f"Failed to verify {display_name}")
        with open(json_results, "w") as f:
            json.dump(results, f, indent=2)

        llm.dump_history(history_dir / f"{file.stem}.txt")


if __name__ == "__main__":
    main()
