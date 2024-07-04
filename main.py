from verus import Verus
from llm import LLM
from invariants import insert_invariants
from modes import Modes, VALID_MODES, precheck
import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("--insert-invariants-mode", help=f"insert invariants using: {', '.join(VALID_MODES)}",
                        default="llm")
    parser.add_argument("--shell", help="shell", default=os.getenv("SHELL"))
    parser.add_argument("--verus-path", help="verus path", default=os.getenv("VERUS_PATH"))
    parser.add_argument("--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN"))
    parser.add_argument("--llm-profile", help="llm profile", default="gpt-4-1106-preview")
    parser.add_argument("--tries", help="number of tries", default=1, type=int)
    args = parser.parse_args()
    mode = Modes(args.insert_invariants_mode)
    if args.input is None:
        args.input = input("Input file: ").strip()
    verus = Verus(args.shell, args.verus_path)
    verified, out, err = verus.verify(args.input)
    if verified:
        print("Verified without modification")
        return
    with open(args.input, "r") as f:
        prg = f.read()
    precheck(prg, mode)
    print("---------------")
    print("Invoking LLM")
    llm = LLM(args.grazie_token, args.llm_profile)
    if mode.is_singlestep:
        inv_prg = llm.rewrite_with_invariants(prg, mode=mode)
    else:
        inv = llm.produce_invariants(prg)
        inv_prg = insert_invariants(llm, prg, inv, mode=mode)
    print("---------------")
    tries = args.tries
    while tries > 0:
        if not os.path.exists("llm-generated"):
            os.mkdir("llm-generated")
        output = f"llm-generated/{args.input[args.input.rfind('/'):]}"
        with open(output, "w") as f:
            f.write(inv_prg)
        verified_inv, out_inv, err_inv = verus.verify(output)
        if verified_inv:
            print("Verified with modification on try", args.tries - tries + 1)
            return
        else:
            print("Verification failed:")
            print(out_inv)
            print(err_inv)
            print("Retrying...")
            tries -= 1
            if tries > 0:
                inv_prg = llm.ask_for_fixed(err_inv)
    print("Failed to verify after", args.tries, "tries")


if __name__ == '__main__':
    main()
