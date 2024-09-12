import logging
import pathlib
import json

from verified_cogen.llm.llm import LLM
from verified_cogen.args import get_default_parser
from verified_cogen.tools import rename_file
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.languages import register_basic_languages
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.validating import ValidatingRunner
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

logger = logging.getLogger(__name__)


def main():
    register_basic_languages()

    parser = get_default_parser()
    parser.add_argument("--filter-by-ext", help="filter by extension", default=None)

    args = parser.parse_args()
    mode = Mode(args.insert_conditions_mode)
    assert mode != Mode.REGEX
    assert args.dir is not None
    assert args.bench_type == "invariants"
    assert args.runs == 1
    assert args.retries == 0

    directory = pathlib.Path(args.dir)
    results_directory = pathlib.Path("results")
    results_directory.mkdir(exist_ok=True)
    json_results = pathlib.Path("results") / f"tries_{directory.name}.json"
    if not json_results.exists():
        with open(json_results, "w") as f:
            json.dump({}, f)
    with open(json_results, "r") as f:
        results = json.load(f)

    if args.filter_by_ext is not None:
        files = list(directory.glob(f"[!.]*.{args.filter_by_ext}"))
    else:
        files = list(directory.glob("[!.]*"))
    assert len(files) > 0, "No files found in the directory"
    files.sort()

    extension = files[0].suffix[1:]
    if (
        different := next((f for f in files if f.suffix[1:] != extension), None)
    ) is not None:
        logger.error(
            f"Found files different extensions: {files[0].name} and {different.name}, please use a single extension"
        )
        return

    language = LanguageDatabase().get(extension)
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
