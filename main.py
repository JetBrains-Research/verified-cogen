from typing_extensions import Optional
from verus import Verus
from llm import LLM
from invariants import insert_invariants
from modes import Mode, VALID_MODES, precheck
import argparse
import pathlib, os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
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
            print("Verification failed:")
            print(out_inv)
            print(err_inv)
            print("Retrying...")
            tries -= 1
            if tries > 0:
                inv_prg = llm.ask_for_fixed(err_inv)
    return None


def invoke_llm(llm: LLM, mode: Mode, prg: str) -> str:
    print("---------------")
    print("Invoking LLM")
    if mode.is_singlestep:
        inv_prg = llm.rewrite_with_invariants(prg, mode=mode)
    else:
        inv = llm.produce_invariants(prg)
        inv_prg = insert_invariants(llm, prg, inv, mode=mode)
    print("---------------")
    return inv_prg


def main():
    args = get_args()
    mode = Mode(args.insert_invariants_mode)
    if args.input is None:
        args.input = input("Input file: ").strip()

    verus = Verus(args.shell, args.verus_path)
    verified, out, err = verus.verify(args.input)
    if verified:
        print("Verified without modification")
        return

    with open(args.input, "r") as input_file:
        prg = input_file.read()
    precheck(prg, mode)

    llm = LLM(args.grazie_token, args.llm_profile, args.temperature)
    inv_prg = invoke_llm(llm, mode, prg)

    if (
        tries := run_llm(verus, llm, args.tries, inv_prg, basename(args.input))
    ) is not None:
        print("Verified with modification on try", tries)
    else:
        print("Failed to verify after", args.tries, "tries")


if __name__ == "__main__":
    main()
