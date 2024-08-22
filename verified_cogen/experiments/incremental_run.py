import pathlib
import logging
from verified_cogen.main import get_args, rename_file
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier
from verified_cogen.llm.llm import LLM
from verified_cogen.runners.invariants import InvariantRunner

logger = logging.getLogger(__name__)


def main():
    args = get_args()
    mode = Mode(args.insert_conditions_mode)
    assert mode != Mode.REGEX
    assert args.dir is not None
    assert args.bench_type == "invariants"
    assert args.runs == 1
    assert args.retries == 0

    directory = pathlib.Path(args.dir)
    marker_directory = directory / f"../tries_{directory.name}"
    marker_directory.mkdir(exist_ok=True, parents=True)
    files = list(directory.glob("[!.]*"))

    verifier = Verifier(args.shell, args.verifier_command)

    for file in files:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )
        display_name = rename_file(file)
        marker_file = marker_directory.joinpath(file.relative_to(directory))
        if marker_file.exists():
            print("Skipping:", display_name)
            continue
        print("Processing:", display_name)
        try:
            tries = InvariantRunner.run_on_file(
                logger, verifier, mode, llm, args.tries, str(file)
            )
        except:
            tries = None
        with marker_file.open("w") as f:
            f.write(str(tries))


if __name__ == "__main__":
    main()
