import json
import logging
import multiprocessing as mp
import pathlib
from typing import Dict, Optional

from verified_cogen.llm.llm import LLM
from verified_cogen.main import construct_rewriter, make_runner_cls
from verified_cogen.runners import Runner, RunnerConfig
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.several_modes.args import ProgramArgsMultiple, get_args
from verified_cogen.several_modes.constants import (
    MODE_MAPPING,
    REMOVE_IMPLS_MAPPING,
    TEXT_DESCRIPTIONS,
)
from verified_cogen.tools import (
    ext_glob,
    extension_from_file_list,
    register_output_handler,
    rename_file,
)
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

logger = logging.getLogger(__name__)


def process_file(
    file: pathlib.Path,
    args: ProgramArgsMultiple,
    history_dir: pathlib.Path,
    llm: LLM,
    rewriter: Rewriter,
    runner: Runner,
) -> Optional[int]:
    try:
        mode = Mode(args.insert_conditions_mode)
        tries = runner.run_on_file(mode, args.tries, str(file))
    except Exception as e:
        print(e)
        tries = None

    llm.dump_history(history_dir / f"{file.stem}.txt")

    return tries


def main():
    args = get_args()
    print(args.manual_rewriters)

    assert args.insert_conditions_mode != Mode.REGEX
    assert args.dir is not None

    if args.output_logging:
        register_output_handler(logger)

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
        all_removed = MODE_MAPPING[mode]
        register_basic_languages(with_removed=all_removed)

        logger.info(mode)
        log_tries_mode = (
            log_tries_dir / f"{idx}_{mode}" if log_tries_dir is not None else None
        )

        if log_tries_mode is not None:
            log_tries_mode.mkdir(exist_ok=True)

        json_avg_results = (
            results_directory / f"tries_{directory.name}_{idx}_{mode}_avg.json"
        )

        with open(json_avg_results, "w") as f:
            json.dump({}, f)
        results_avg: Dict[int, float] = dict([(i, 0) for i in range(args.tries + 1)])

        for run in range(args.runs):
            logger.info(f"Run {run}")

            history_dir = (
                results_directory / f"history_{directory.name}_{idx}_{mode}_{run}"
            )
            history_dir.mkdir(exist_ok=True)
            json_results = (
                results_directory / f"tries_{directory.name}_{idx}_{mode}_{run}.json"
            )

            if not json_results.exists():
                with open(json_results, "w") as f:
                    json.dump({}, f)

            with open(json_results, "r") as f:
                results = json.load(f)

            log_tries = log_tries_mode and (log_tries_mode / f"run_{run}")
            if log_tries is not None:
                log_tries.mkdir(exist_ok=True)

            config = RunnerConfig(
                log_tries=log_tries,
                include_text_descriptions=TEXT_DESCRIPTIONS[mode],
                remove_implementations=REMOVE_IMPLS_MAPPING[mode],
                remove_helpers=(mode == "mode6"),
            )

            files_to_process: list[tuple[pathlib.Path, str, str]] = []
            for file in files:
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
                files_to_process.append((file, display_name, marker_name))

            llm = LLM(
                args.grazie_token,
                args.llm_profile,
                args.prompts_directory[idx],
                args.temperature,
            )

            rewriter = construct_rewriter(
                extension_from_file_list(files), args.manual_rewriters
            )

            runner = make_runner_cls(
                args.bench_type, extension_from_file_list(files), config
            )(llm, logger, verifier, rewriter)

            with mp.Pool(processes=mp.cpu_count()) as pool:

                def make_arguments(file: pathlib.Path):
                    return file, args, history_dir, llm, rewriter, runner

                mp_results = pool.starmap(
                    process_file,
                    (make_arguments(file) for file, _, _ in files_to_process),
                )

            for (file, display_name, marker_name), tries in zip(
                files_to_process, mp_results
            ):
                logger.info(f"Processing results for: {display_name}")

                if tries is not None:
                    results[marker_name] = tries
                    results_avg[tries] += 1
                    logger.info(f"Verified {display_name} in {tries} tries")
                else:
                    results[marker_name] = -1
                    logger.info(f"Failed to verify {display_name}")
                with open(json_results, "w") as f:
                    json.dump(results, f, indent=2)

        for key in results_avg.keys():
            results_avg[key] = results_avg[key] / args.runs

        with open(json_avg_results, "w") as f:
            json.dump(results_avg, f)

        logger.info(f"Averaged results for {mode}: {results_avg}")


if __name__ == "__main__":
    main()
