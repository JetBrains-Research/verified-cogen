import json
import logging
import multiprocessing as mp
import os
import pathlib
from dataclasses import dataclass
from multiprocessing.managers import DictProxy, SyncManager
from threading import Lock
from typing import Optional

import click

from verified_cogen.args import IOConfig, LLMConfig, ProgramConfig
from verified_cogen.runners import RunnerConfig
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType
from verified_cogen.runners.make_runner import make_runner_cls
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.runners.rewriters.construct import construct_rewriter
from verified_cogen.several_modes.constants import (
    MODE_MAPPING,
    REMOVE_IMPLS_MAPPING,
    TEXT_DESCRIPTIONS,
    VALID_BENCH_TYPES,
)
from verified_cogen.tools import (
    ext_glob,
    extension_from_file_list,
    make_split_commas,
    register_output_handler,
    rename_file,
)
from verified_cogen.tools.modes import VALID_MODES, Mode
from verified_cogen.tools.throttle import Throttle
from verified_cogen.tools.verifier import Verifier

logger = logging.getLogger(__name__)


@dataclass
class Tools:
    rewriter: Optional[Rewriter]
    verifier: Verifier
    runner: RunnerConfig


@dataclass
class ProcessFileConfig:
    program: ProgramConfig
    history_dir: pathlib.Path
    json_results: pathlib.Path
    extension: str

    all_removed: list[AnnotationType]
    tools: Tools


@dataclass
class SharedState:
    lock: Lock
    results: "DictProxy[str, int]"


def process_file(
    config: ProcessFileConfig,
    file_with_name: tuple[pathlib.Path, str],
    state: SharedState,
    idx: int,
) -> Optional[int]:
    register_basic_languages(with_removed=config.all_removed)
    file, marker_name = file_with_name

    llm = config.program.llm.build(
        idx,
        history=config.history_dir / f"{file.stem}.txt",
    )
    runner = make_runner_cls(config.program.bench_types[idx], config.extension, config.tools.runner)(
        llm, logger, config.tools.verifier, config.tools.rewriter
    )
    try:
        mode = Mode(config.program.insert_conditions_mode)
        tries = runner.run_on_file(mode, config.program.tries, str(file))
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
    runner.dump_history(config.history_dir / f"{file.stem}_valid.json")

    return tries


def run_mode(
    manager: SyncManager,
    config: ProgramConfig,
    idx: int,
    mode: str,
    files: list[pathlib.Path],
    verifier: Verifier,
):
    all_removed = MODE_MAPPING[mode]
    register_basic_languages(with_removed=all_removed)

    logger.info(mode)
    log_tries_mode = config.log_tries_directory / f"{idx}_{mode}" if config.log_tries_directory is not None else None

    if log_tries_mode is not None:
        log_tries_mode.mkdir(exist_ok=True)

    json_avg_results = config.results_directory / f"tries_{config.directory.name}_{idx}_{mode}_avg.json"

    with open(json_avg_results, "w") as f:
        json.dump({}, f)

    results_avg: dict[int, float] = {i: 0 for i in range(config.tries + 1)}
    lock = manager.Lock()

    for run in range(config.runs):
        logger.info(f"Run {run}")

        history_dir = config.results_directory / f"history_{config.directory.name}_{idx}_{mode}_{run}"
        history_dir.mkdir(exist_ok=True)
        json_results = config.results_directory / f"tries_{config.directory.name}_{idx}_{mode}_{run}.json"

        if not json_results.exists():
            with open(json_results, "w") as f:
                json.dump({}, f)

        with open(json_results) as f:
            results = manager.dict(json.load(f))

        log_tries = log_tries_mode and (log_tries_mode / f"run_{run}")
        if log_tries is not None:
            log_tries.mkdir(exist_ok=True)

        runner_config = RunnerConfig(
            log_tries=log_tries,
            include_text_descriptions=TEXT_DESCRIPTIONS[mode],
            remove_implementations=REMOVE_IMPLS_MAPPING[mode],
            remove_helpers=(mode == "mode6"),
            record_history=True,
        )

        files_to_process: list[tuple[pathlib.Path, str]] = []
        for file in files:
            display_name = rename_file(file)
            marker_name = str(file.relative_to(config.directory))
            if marker_name in results and isinstance(results[marker_name], int):
                if results[marker_name] != -1:
                    logger.info(f"Skipping: {display_name} as it has already been verified")
                    continue
                elif results[marker_name] == -1 and config.io.skip_failed:
                    logger.info(f"Skipping: {display_name} as it has not been verified and is marked as failed")
                    continue
            files_to_process.append((file, marker_name))

        rewriter = construct_rewriter(
            extension_from_file_list(files),
            (config.llm, idx),
            config.manual_rewriters,
        )

        state = SharedState(lock, results)
        with mp.Pool(processes=min(config.io.max_jobs, mp.cpu_count())) as pool:
            process_config = ProcessFileConfig(
                config,
                history_dir,
                json_results,
                extension_from_file_list(files),
                all_removed,
                Tools(rewriter, verifier, runner_config),
            )

            pool.starmap(
                process_file,
                ((process_config, (file, marker_name), state, idx) for file, marker_name in files_to_process),
            )

        for v in state.results.values():
            if v != -1:
                results_avg[v] += 1

    for key in results_avg:
        results_avg[key] = results_avg[key] / config.runs

    with open(json_avg_results, "w") as f:
        json.dump(dict(results_avg), f)

    logger.info(f"Averaged results for {mode}: {results_avg}")


@click.command()
@click.option("-d", "--dir", required=True, type=click.Path(), prompt=True)
@click.option("--filter-by-ext")
@click.option("-r", "--runs", help="number of runs", default=1)
@click.option("-j", "--max-jobs", help="parallel jobs limit", default=mp.cpu_count())
@click.option("--tries", default=1)
@click.option("--modes", multiple=True, default=[], callback=make_split_commas())
@click.option("--insert-conditions-mode", default="llm-single-step", type=click.Choice(VALID_MODES))
@click.option(
    "--bench-types",
    multiple=True,
    default=[],
    callback=make_split_commas(VALID_BENCH_TYPES),
)
@click.option("--manual-rewriters", multiple=True, default=[], callback=make_split_commas())
@click.option("--llm-profile", default="gpt-4-1106-preview")
@click.option("-t", "--temperature", type=float, help="model temperature", default=0)
@click.option("--grazie-token", default=lambda: os.getenv("GRAZIE_JWT_TOKEN"))
@click.option("--prompts-directory", multiple=True, default=[], callback=make_split_commas())
@click.option(
    "--verifier-command",
    help="command to run (cmd [file_path]) to verify a file",
    default=lambda: os.getenv("VERIFIER_COMMAND"),
)
@click.option(
    "--test-command",
    help="command to run (cmd [file_path]) to run tests on a file",
    default=lambda: None,
)
@click.option(
    "--verifier-timeout",
    help="timeout for verifier command",
    default=60,
)
@click.option("--skip-failed", is_flag=True, default=False)
@click.option("--log-tries")
@click.option("--output-logging", is_flag=True, default=False)
@click.option("--rate-limit", help="Number of requests allowed per window", type=int, default=None)
@click.option("--rate-window", help="Time window in seconds for rate limiting", type=int, default=None)
def main(
    dir: str,
    filter_by_ext: Optional[str],
    runs: int,
    max_jobs: int,
    tries: int,
    modes: list[str],
    insert_conditions_mode: str,
    bench_types: list[str],
    manual_rewriters: list[str],
    llm_profile: str,
    temperature: float,
    grazie_token: str,
    prompts_directory: list[str],
    verifier_command: str,
    test_command: str,
    verifier_timeout: int,
    skip_failed: bool,
    log_tries: Optional[str],
    output_logging: bool,
    rate_limit: Optional[int],
    rate_window: Optional[int],
):
    assert insert_conditions_mode != Mode.REGEX

    if output_logging:
        register_output_handler(logger)

    log_tries_directory = pathlib.Path(log_tries) if log_tries is not None else None
    if log_tries_directory is not None:
        log_tries_directory.mkdir(exist_ok=True)

    directory = pathlib.Path(dir)
    files = list(directory.glob(ext_glob(filter_by_ext)))
    assert len(files) > 0, "No files found in the directory"
    files.sort()

    results_directory = pathlib.Path("results")
    results_directory.mkdir(exist_ok=True)

    verifier = Verifier(verifier_command, test_command, verifier_timeout)

    logger.info(f"LLM token: {grazie_token[:3]}...{grazie_token[-3:]}")

    with mp.Manager() as manager:
        throttle = Throttle(manager, rate_limit, rate_window)
        config = ProgramConfig(
            directory,
            tries,
            runs,
            insert_conditions_mode,
            bench_types,
            manual_rewriters,
            log_tries_directory,
            results_directory,
            LLMConfig(temperature, grazie_token, llm_profile, prompts_directory, throttle),
            IOConfig(max_jobs, skip_failed),
        )
        for idx, mode in enumerate(modes):
            run_mode(manager, config, idx, mode, files, verifier)


if __name__ == "__main__":
    main()
