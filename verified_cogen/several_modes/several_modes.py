import json
import logging
import multiprocessing as mp
import pathlib
from dataclasses import dataclass
from multiprocessing.managers import DictProxy, SyncManager
from threading import Lock
from typing import Optional

from verified_cogen.llm.llm import LLM
from verified_cogen.main import construct_rewriter, make_runner_cls
from verified_cogen.runners import RunnerConfig
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType
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


@dataclass
class ProcessFileConfig:
    args: ProgramArgsMultiple
    history_dir: pathlib.Path
    json_results: pathlib.Path
    extension: str


@dataclass
class SharedState:
    lock: Lock
    results: "DictProxy[str, int]"


def process_file(
    file_with_name: tuple[pathlib.Path, str],
    rewriter: Optional[Rewriter],
    verifier: Verifier,
    runner_config: RunnerConfig,
    config: ProcessFileConfig,
    state: SharedState,
    idx: int,
    all_removed: list[AnnotationType],
) -> Optional[int]:
    register_basic_languages(with_removed=all_removed)
    llm = LLM(
        config.args.grazie_token,
        config.args.llm_profile,
        config.args.prompts_directory[idx],
        config.args.temperature,
    )
    runner = make_runner_cls(config.args.bench_types[idx], config.extension, runner_config)(
        llm, logger, verifier, rewriter
    )
    file, marker_name = file_with_name
    try:
        mode = Mode(config.args.insert_conditions_mode)
        tries = runner.run_on_file(mode, config.args.tries, str(file))
    except Exception as e:
        print(e)
        tries = None

    display_name = rename_file(file)
    with state.lock:
        if tries is not None:
            state.results[marker_name] = tries
            logger.info(f"Verified {display_name} in {tries} tries")
        else:
            state.results[marker_name] = -1
            logger.info(f"Failed to verify {display_name}")
        with open(config.json_results, "w") as f:
            json.dump(dict(state.results), f, indent=2)

    llm.dump_history(config.history_dir / f"{file.stem}.txt")

    return tries


def run_mode(
    manager: SyncManager,
    idx: int,
    mode: str,
    directory: pathlib.Path,
    files: list[pathlib.Path],
    args: ProgramArgsMultiple,
    results_directory: pathlib.Path,
    verifier: Verifier,
    log_tries_dir: Optional[pathlib.Path],
):
    all_removed = MODE_MAPPING[mode]
    register_basic_languages(with_removed=all_removed)

    logger.info(mode)
    log_tries_mode = log_tries_dir / f"{idx}_{mode}" if log_tries_dir is not None else None

    if log_tries_mode is not None:
        log_tries_mode.mkdir(exist_ok=True)

    json_avg_results = results_directory / f"tries_{directory.name}_{idx}_{mode}_avg.json"

    with open(json_avg_results, "w") as f:
        json.dump({}, f)

    results_avg: "dict[int, float]" = {i: 0 for i in range(args.tries + 1)}
    lock = manager.Lock()

    for run in range(args.runs):
        logger.info(f"Run {run}")

        history_dir = results_directory / f"history_{directory.name}_{idx}_{mode}_{run}"
        history_dir.mkdir(exist_ok=True)
        json_results = results_directory / f"tries_{directory.name}_{idx}_{mode}_{run}.json"

        if not json_results.exists():
            with open(json_results, "w") as f:
                json.dump({}, f)

        with open(json_results, "r") as f:
            results = manager.dict(json.load(f))

        log_tries = log_tries_mode and (log_tries_mode / f"run_{run}")
        if log_tries is not None:
            log_tries.mkdir(exist_ok=True)

        runner_config = RunnerConfig(
            log_tries=log_tries,
            include_text_descriptions=TEXT_DESCRIPTIONS[mode],
            remove_implementations=REMOVE_IMPLS_MAPPING[mode],
            remove_helpers=(mode == "mode6"),
        )

        files_to_process: list[tuple[pathlib.Path, str, str]] = []
        for file in files:
            display_name = rename_file(file)
            marker_name = str(file.relative_to(directory))
            if marker_name in results and isinstance(results[marker_name], int) and results[marker_name] != -1:
                logger.info(f"Skipping: {display_name} as it has already been verified")
                continue
            files_to_process.append((file, display_name, marker_name))

        rewriter = construct_rewriter(extension_from_file_list(files), args.manual_rewriters)

        state = SharedState(lock, results)
        with mp.Pool(processes=min(args.max_jobs, mp.cpu_count())) as pool:
            config = ProcessFileConfig(args, history_dir, json_results, extension_from_file_list(files))

            def make_arguments(file: pathlib.Path, marker_name: str):
                return (
                    (file, marker_name),
                    rewriter,
                    verifier,
                    runner_config,
                    config,
                    state,
                    idx,
                    all_removed,
                )

            arguments = (make_arguments(file, marker_name) for file, _, marker_name in files_to_process)
            pool.starmap(process_file, arguments)

        for v in state.results.values():
            if v != -1:
                results_avg[v] += 1

    for key in results_avg.keys():
        results_avg[key] = results_avg[key] / args.runs

    with open(json_avg_results, "w") as f:
        json.dump(dict(results_avg), f)

    logger.info(f"Averaged results for {mode}: {results_avg}")


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

    with mp.Manager() as manager:
        for idx, mode in enumerate(args.modes):
            run_mode(
                manager,
                idx,
                mode,
                directory,
                files,
                args,
                results_directory,
                verifier,
                log_tries_dir,
            )


if __name__ == "__main__":
    main()
