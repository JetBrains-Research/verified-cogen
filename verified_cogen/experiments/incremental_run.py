import logging
import pathlib
import json

from verified_cogen.llm.llm import LLM
from verified_cogen.args import get_args
from verified_cogen.tools import rename_file, ext_glob, extension_from_file_list, register_output_handler
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.validating import ValidatingRunner
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

logger = logging.getLogger(__name__)


def main():
    register_basic_languages()

    args = get_args()
    mode = Mode(args.insert_conditions_mode)
    assert mode != Mode.REGEX
    assert args.dir is not None
    assert args.bench_type == "validating", args.bench_type
    assert args.runs == 1
    assert args.retries == 0

    if args.output_logging:
        register_output_handler(logger)

    directory = pathlib.Path(args.dir)
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

    language = LanguageDatabase().get(extension_from_file_list(files))
    verifier = Verifier(args.shell, args.verifier_command)

    for file in files:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )
        runner = ValidatingRunner(
            wrapping=InvariantRunner(llm, logger, verifier),
            language=language,
            log_tries=log_tries,
        )
        display_name = rename_file(file)
        marker_name = str(file.relative_to(directory))
        if marker_name in results and isinstance(results[marker_name], int):
            logger.info(f"Skipping: {display_name} as it has already been verified")
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
            logger.info(f"Failed to verify {display_name}")
        with open(json_results, "w") as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
