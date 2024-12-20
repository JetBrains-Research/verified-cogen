import json
import logging
import pathlib
from typing import Dict

from verified_cogen.several_modes.args import get_default_parser_multiple
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


logger = logging.getLogger(__name__)


def main():
    parser = get_default_parser_multiple()
    parser.add_argument(
        "--ignore-failed", help="Ignore failed files", action="store_true"
    )
    args = parser.parse_args()
    print(args.manual_rewriters)

    assert args.insert_conditions_mode != Mode.REGEX
    assert args.dir is not None

    mode_mapping = {
        "mode1": [AnnotationType.INVARIANTS, AnnotationType.ASSERTS],
        "mode2": [
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.PRE_CONDITIONS,
            AnnotationType.POST_CONDITIONS,
        ],
        "mode3": [
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.IMPLS,
        ],
        "mode4": [
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.IMPLS,
        ],
        "mode5": [
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.PRE_CONDITIONS,
            AnnotationType.POST_CONDITIONS,
            AnnotationType.IMPLS,
        ],
        "mode6": [
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.PRE_CONDITIONS,
            AnnotationType.POST_CONDITIONS,
            AnnotationType.IMPLS,
            AnnotationType.PURE,
        ],
    }

    remove_impls_mapping = {
        "mode1": False,
        "mode2": False,
        "mode3": True,
        "mode4": True,
        "mode5": True,
        "mode6": True,
    }

    text_descriptions = {
        "mode1": False,
        "mode2": False,
        "mode3": False,
        "mode4": True,
        "mode5": True,
        "mode6": True,
    }

    if args.output_logging:
        register_output_handler(logger)

    mode_insert_conditions = Mode(args.insert_conditions_mode)

    log_tries_dir = pathlib.Path(args.log_tries) if args.log_tries is not None else None
    if log_tries_dir is not None:
        log_tries_dir.mkdir(exist_ok=True)

    directory = pathlib.Path(args.dir)
    files = list(directory.glob(ext_glob(args.filter_by_ext)))
    assert len(files) > 0, "No files found in the directory"
    files.sort()

    results_directory = pathlib.Path("results")
    results_directory.mkdir(exist_ok=True)

    verifier = Verifier(args.verifier_command)

    for idx, mode in enumerate(args.modes):
        all_removed = mode_mapping[mode]
        register_basic_languages(with_removed=all_removed)

        logger.info(mode)
        log_tries_mode = log_tries_dir / mode if log_tries_dir is not None else None
        if log_tries_mode is not None:
            log_tries_mode.mkdir(exist_ok=True)

        json_avg_results = results_directory / f"tries_{directory.name}_{mode}_avg.json"
        with open(json_avg_results, "w") as f:
            json.dump({}, f)
        results_avg: Dict[int, float] = dict([(i, 0) for i in range(args.runs)])

        for run in range(args.runs):
            logger.info(f"Run {run}")

            history_dir = results_directory / f"history_{directory.name}_{mode}_{run}"
            history_dir.mkdir(exist_ok=True)
            json_results = (
                results_directory / f"tries_{directory.name}_{mode}_{run}.json"
            )
            if not json_results.exists():
                with open(json_results, "w") as f:
                    json.dump({}, f)
            with open(json_results, "r") as f:
                results = json.load(f)

            log_tries = (
                log_tries_mode / f"run_{run}" if log_tries_mode is not None else None
            )
            if log_tries is not None:
                log_tries.mkdir(exist_ok=True)

            config = RunnerConfig(
                log_tries=log_tries,
                include_text_descriptions=text_descriptions[mode],
                remove_implementations=remove_impls_mapping[mode],
                remove_helpers=mode == "mode6",
            )

            for file in files:
                llm = LLM(
                    args.grazie_token,
                    args.llm_profile,
                    args.prompts_directory[idx],
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
                    logger.info(
                        f"Skipping: {display_name} as it has already been verified"
                    )
                    continue
                logger.info(f"Processing: {display_name}")
                try:
                    tries = runner.run_on_file(
                        mode_insert_conditions, args.tries, str(file)
                    )
                except KeyboardInterrupt:
                    return
                except Exception as e:
                    print(e)
                    tries = None
                if tries is not None:
                    results[marker_name] = tries
                    results_avg[tries] += 1
                    logger.info(f"Verified {display_name} in {tries} tries")
                else:
                    results[marker_name] = -1
                    logger.info(f"Failed to verify {display_name}")
                with open(json_results, "w") as f:
                    json.dump(results, f, indent=2)

                llm.dump_history(history_dir / f"{file.stem}.txt")

        for key in results_avg.keys():
            results_avg[key] = results_avg[key] / args.runs

        with open(json_avg_results, "w") as f:
            json.dump(results_avg, f)

        logger.info(f"Averaged results for {mode}: {results_avg}")


if __name__ == "__main__":
    main()
