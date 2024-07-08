from tqdm import tqdm
from typing_extensions import Optional
from verus import Verus
from llm import LLM
from invariants import insert_invariants
from modes import Mode, VALID_MODES, precheck
import argparse
import pathlib
import os
import logging

logging.basicConfig(
    level=os.environ.get('PYLOG_LEVEL', 'INFO').upper()
)
logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("-d", "--dir", help="directory to run on", required=False)

    parser.add_argument(
        "--insert-invariants-mode",
        help=f"insert invariants using: {', '.join(VALID_MODES)}",
        default="llm",
    )
    parser.add_argument("--temperature", help="model temperature", default=0, type=int)
    parser.add_argument("--shell", help="shell", default=os.getenv("SHELL"))
    parser.add_argument(
        "--verus-path", help="verus path", default=os.getenv("VERUS_PATH")
    )
    parser.add_argument(
        "--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN")
    )
    parser.add_argument(
        "--llm-profile", help="llm profile", default="gpt-4-1106-preview"
    )
    parser.add_argument("--tries", help="number of tries", default=1, type=int)
    parser.add_argument("-s", "--output-style", choices=["stats", "full"], default="full")
    return parser.parse_args()


def basename(path: str):
    return pathlib.Path(path).name


def run_llm(
        verus: Verus, llm: LLM, total_tries: int, inv_prg: str, name: str
) -> Optional[int]:
    tries = total_tries
    while tries > 0:
        if not os.path.exists("llm-generated"):
            os.mkdir("llm-generated")
        output = f"llm-generated/{name}"
        with open(output, "w") as f:
            f.write(inv_prg)
        verified_inv, out_inv, err_inv = verus.verify(output)
        if verified_inv:
            return total_tries - tries + 1
        else:
            logger.info("Verification failed:")
            logger.info(out_inv)
            logger.info(err_inv)
            logger.info("Retrying...")
            tries -= 1
            if tries > 0:
                inv_prg = llm.ask_for_fixed(err_inv)
    return None


def invoke_llm(llm: LLM, mode: Mode, prg: str) -> str:
    logger.info("Invoking LLM")
    if mode.is_singlestep:
        inv_prg = llm.rewrite_with_invariants(prg, mode=mode)
    else:
        inv = llm.produce_invariants(prg)
        inv_prg = insert_invariants(llm, prg, inv, mode=mode)
    logger.info("Invocation done")
    return inv_prg


def run_on_file(
        verus: Verus,
        mode: Mode,
        llm: LLM,
        total_tries: int,
        file: str,
) -> Optional[int]:
    logger.info(f"Running on {file}")

    verified, out, err = verus.verify(file)
    if verified:
        logger.info("Verified without modification")
        return 0

    with open(file, "r") as input_file:
        prg = input_file.read()
    precheck(prg, mode)

    inv_prg = invoke_llm(llm, mode, prg)

    tries = run_llm(verus, llm, total_tries, inv_prg, basename(file))
    if tries is not None:
        logger.info(f"Verified with modification on try {tries}")
    else:
        logger.error(f"Failed to verify {file} after {total_tries} tries")
    return tries


def rename_file(file: pathlib.Path) -> str:
    return " ".join(file.stem.split("_")).title()


def main():
    args = get_args()
    mode = Mode(args.insert_invariants_mode)
    if args.input is None and args.dir is None:
        args.input = input("Input file: ").strip()

    verus = Verus(args.shell, args.verus_path)
    if args.dir is not None:
        success, success_zero_tries, failed = [], [], []

        files = list(pathlib.Path(args.dir).glob("**/*.rs"))
        for file in tqdm(files):
            llm = LLM(args.grazie_token, args.llm_profile, args.temperature)
            tries = run_on_file(verus, mode, llm, args.tries, str(file))
            if tries == 0:
                success_zero_tries.append(rename_file(file))
            elif tries is not None:
                success.append(rename_file(file))
            else:
                failed.append(rename_file(file))
        if args.output_style == "full":
            success_zero_tries_tabbed = "\n\t - " + "\n\t - ".join(success_zero_tries)
            success_tabbed = "\n\t - " + "\n\t - ".join(success)
            failed_tabbed = "\n\t - " + "\n\t - ".join(failed)
            if len(success_zero_tries) > 0:
                print(f"Without modification: {success_zero_tries_tabbed}")
            if len(success) > 0:
                print(f"With modification: {success_tabbed}")
            if len(failed) > 0:
                print(f"Failed: {failed_tabbed}")
        print(
            "Verified without modification: {} ({:.2f}%)".format(
                len(success_zero_tries),
                len(success_zero_tries) / len(files) * 100,
            )
        )
        print(
            "Verified with modification: {} ({:.2f}%)".format(
                len(success),
                len(success) / len(files) * 100,
            )
        )
        print(
            "Failed: {} ({:.2f}%)".format(
                len(failed),
                len(failed) / len(files) * 100,
            )
        )
    else:
        llm = LLM(args.grazie_token, args.llm_profile, args.temperature)
        run_on_file(verus, mode, llm, args.tries, args.input)


if __name__ == "__main__":
    main()
