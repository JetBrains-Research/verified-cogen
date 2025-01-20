import json
import logging
import pathlib

from verified_cogen.smart_search.args import get_args, ProgramArgsSearch
from verified_cogen.llm.llm import LLM
from verified_cogen.main import make_runner_cls
from verified_cogen.runners import RunnerConfig, Runner
from verified_cogen.runners.languages import AnnotationType, register_basic_languages
from verified_cogen.smart_search.scoring_functions import ScoringFunction
from verified_cogen.smart_search.scoring_functions.nagini_simple import (
    NaginiSimpleScoringFunction,
)
from verified_cogen.smart_search.search_algos import SearchAlgo
from verified_cogen.smart_search.search_algos.rebase import Rebase
from verified_cogen.tools import (
    ext_glob,
    extension_from_file_list,
    register_output_handler,
    rename_file,
    get_cache_dir,
)
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.tree_painter import paint_tree
from verified_cogen.tools.verifier import Verifier


logger = logging.getLogger(__name__)


def make_scoring_fun(args: ProgramArgsSearch) -> ScoringFunction:
    if args.scoring_fun == "NaginiSimple":
        return NaginiSimpleScoringFunction(args.error_penalty, args.long_penalty)
    else:
        raise NotImplementedError("this scoring function is not implemented")


def make_algo(
    args: ProgramArgsSearch,
    runner: Runner,
    mode: Mode,
    scoring_function: ScoringFunction,
) -> SearchAlgo:
    if args.search_algo == "rebase":
        return Rebase(args.width, args.depth, runner, mode, scoring_function)
    else:
        raise NotImplementedError("this search algorithm is not implemented")


def main():
    args = get_args()
    all_removed = [AnnotationType.INVARIANTS, AnnotationType.ASSERTS]
    if args.remove_implementations:
        all_removed += [AnnotationType.IMPLS]

    register_basic_languages(with_removed=all_removed)
    mode = Mode(args.insert_conditions_mode)

    if args.output_logging:
        register_output_handler(logger)

    assert args.insert_conditions_mode != Mode.REGEX
    assert args.dir is not None

    log_tries = pathlib.Path(args.log_tries) if args.log_tries is not None else None

    verifier = Verifier(args.verifier_command, args.verifier_timeout)
    config = RunnerConfig(
        log_tries=log_tries,
        include_text_descriptions=args.include_text_descriptions,
        remove_implementations=args.remove_implementations,
    )

    files = sorted(list(pathlib.Path(args.dir).glob(ext_glob(args.filter_by_ext))))
    runner_cls = make_runner_cls(
        args.bench_type, extension_from_file_list(files), config
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
        None,
    )
    for file in files:
        with open(file) as f:
            runner.precheck(f.read(), mode)

    scoring_fun = make_scoring_fun(args)

    results_directory = pathlib.Path("results")
    results_directory.mkdir(exist_ok=True)

    json_depth_results = (
        results_directory / f"tries_{pathlib.Path(args.dir).name}_depth.json"
    )
    json_total_results = (
        results_directory / f"tries_{pathlib.Path(args.dir).name}_total.json"
    )

    if not json_depth_results.exists():
        with open(json_depth_results, "w") as f:
            json.dump({}, f)
    with open(json_depth_results, "r") as f:
        depth_results = json.load(f)

    if not json_total_results.exists():
        with open(json_total_results, "w") as f:
            json.dump({}, f)
    with open(json_total_results, "r") as f:
        total_results = json.load(f)

    graph_dir = pathlib.Path(get_cache_dir()) / "graphs"
    graph_dir.mkdir(exist_ok=True)

    history_path = pathlib.Path(get_cache_dir()) / "history_smart"
    history_path.mkdir(exist_ok=True)

    for file in files:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )

        runner = runner_cls(llm, logger, verifier, None)
        algo = make_algo(args, runner, mode, scoring_fun)

        depth, total = algo.run_on_file(str(file))

        name = rename_file(file)
        depth_results[name] = depth
        total_results[name] = total

        with open(json_depth_results, "w") as f:
            json.dump(depth_results, f, indent=2)

        with open(json_total_results, "w") as f:
            json.dump(total_results, f, indent=2)

        edges = algo.tree.collect_edges()
        paint_tree(edges, graph_dir / f"{name}.png")

        algo.tree.dump_history(history_path)
        # llm.dump_history(pathlib.Path(get_cache_dir()) / "history" / f"{name}.txt")


if __name__ == "__main__":
    main()
