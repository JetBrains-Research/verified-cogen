import logging
import pathlib

from verified_cogen.llm.llm import LLM
from verified_cogen.main import get_args, rename_file
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
    assert args.bench_type == "invariants"
    assert args.runs == 1
    assert args.retries == 0

    directory = pathlib.Path(args.dir)
    marker_directory = pathlib.Path(f"results/tries_{directory.name}")
    marker_directory.mkdir(exist_ok=True, parents=True)
    files = list(directory.glob("[!.]*.dfy"))
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
            language=LanguageDatabase().get("dfy"),
        )
        display_name = rename_file(file)
        marker_file = marker_directory.joinpath(file.relative_to(directory))
        if marker_file.exists():
            print("Skipping:", display_name)
            continue
        print("Processing:", display_name)
        try:
            tries = runner.run_on_file(mode, args.tries, str(file))
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)
            tries = None
        with marker_file.open("w") as f:
            f.write(str(tries))


if __name__ == "__main__":
    main()
