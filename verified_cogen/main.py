import argparse
import logging
import os
import pathlib

from tqdm import tqdm

from verified_cogen.runners.generic import GenericRunner
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.llm import LLM
from verified_cogen.tools import pprint_stat, rename_file, tabulate_list
from verified_cogen.tools.modes import VALID_MODES, Mode
from verified_cogen.tools.verifier import Verifier

logger = logging.getLogger(__name__)


def run_once(args, runner, verifier, mode, is_once) -> tuple[int, int, int]:
    success, success_zero_tries, failed = [], [], []

    files = list(pathlib.Path(args.dir).glob("**/*"))
    print(files)
    for file in tqdm(files):
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )

        retries = args.retries + 1
        tries = None
        while retries > 0 and tries is None:
            tries = runner.run_on_file(
                logger, verifier, mode, llm, args.tries, str(file)
            )
            retries -= 1

        name = rename_file(file)
        if tries == 0:
            logger.info(f"{name} verified without modification")
            success_zero_tries.append(name)
        elif tries is not None:
            logger.info(f"{name} verified with modification")
            success.append(name)
        else:
            logger.error(f"{name} failed")
            failed.append(name)

    if is_once:
        if args.output_style == "full":
            success_zero_tries_tabbed = tabulate_list(success_zero_tries)
            success_tabbed = tabulate_list(success)
            failed_tabbed = tabulate_list(failed)
            if len(success_zero_tries) > 0:
                print(f"Verified without modification: {success_zero_tries_tabbed}")
            if len(success) > 0:
                print(f"Verified with modification: {success_tabbed}")
            if len(failed) > 0:
                print(f"Failed: {failed_tabbed}")

        pprint_stat(
            "Verified without modification", len(success_zero_tries), len(files)
        )
        pprint_stat("Verified with modification", len(success), len(files))
        pprint_stat("Failed", len(failed), len(files))

    return len(success_zero_tries), len(success), len(failed)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("-d", "--dir", help="directory to run on", required=False)

    parser.add_argument("-r", "--runs", help="number of runs", default=1, type=int)

    parser.add_argument(
        "--insert-conditions-mode",
        help=f"insert conditions using: {', '.join(VALID_MODES)}",
        default="llm",
    )
    parser.add_argument(
        "--bench-type",
        help="benchmark type, available: {invariants, generic}",
        default="invariants",
    )
    parser.add_argument("--temperature", help="model temperature", default=0, type=int)
    parser.add_argument("--shell", help="shell", default=os.getenv("SHELL"))
    parser.add_argument(
        "--verifier-command",
        help="command to run (cmd [file_path]) to verify a file",
        default=os.getenv("VERIFIER_COMMAND"),
    )
    parser.add_argument(
        "--prompts-directory",
        help="directory containing prompts",
        default=os.getenv("llm/prompts"),
    )
    parser.add_argument(
        "--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN")
    )
    parser.add_argument(
        "--llm-profile", help="llm profile", default="gpt-4-1106-preview"
    )
    parser.add_argument("--tries", help="number of tries", default=1, type=int)
    parser.add_argument("--retries", help="number of retries", default=0, type=int)
    parser.add_argument(
        "-s", "--output-style", choices=["stats", "full"], default="full"
    )
    return parser.parse_args()


def main():
    args = get_args()
    mode = Mode(args.insert_conditions_mode)
    if mode == Mode.REGEX:
        if "dafny" not in args.verifier_command:
            raise ValueError("Regex mode only works with Dafny verifier")

        if args.bench_type == "generic":
            raise ValueError("Regex mode only works with invariants")

    if args.input is None and args.dir is None:
        args.input = input("Input file: ").strip()

    runner = InvariantRunner if args.bench_type == "invariants" else GenericRunner

    verifier = Verifier(args.shell, args.verifier_command)
    if args.dir is not None:
        if args.runs == 1:
            run_once(args, runner, verifier, mode, is_once=True)
        else:
            success_zero_tries, success, failed = 0, 0, 0
            for _ in range(args.runs):
                s0, s, f = run_once(args, runner, verifier, mode, is_once=False)
                success_zero_tries += s0
                success += s
                failed += f

            pprint_stat("Verified without modification", success_zero_tries, args.runs)
            pprint_stat("Verified with modification", success, args.runs)
            pprint_stat("Failed", failed, args.runs)
    else:
        llm = LLM(
            args.grazie_token,
            args.llm_profile,
            args.prompts_directory,
            args.temperature,
        )
        tries = runner.run_on_file(logger, verifier, mode, llm, args.tries, args.input)
        if tries == 0:
            print("Verified without modification")
        elif tries is not None:
            print("Verified with modification on try", tries)
        else:
            print("Failed to verify")
