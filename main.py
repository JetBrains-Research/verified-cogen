from dafny import Dafny
from llm.llm import LLM
from invariants import insert_invariants
from modes import Modes, VALID_MODES, precheck
import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("--insert-invariants-mode", help=f"insert invariants using: {', '.join(VALID_MODES)}", default="llm")
    parser.add_argument("--dafny-path", help="dafny path", default="dafny")
    parser.add_argument("--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN"))
    parser.add_argument("--llm-profile", help="llm profile", default="gpt-4-1106-preview")
    args = parser.parse_args()
    mode = Modes(args.insert_invariants_mode)
    if args.input is None:
        args.input = input("Input file: ")
    dafny = Dafny(args.dafny_path)
    verified, msg = dafny.verify(args.input)
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
        inv_prg = insert_invariants(dafny, llm, prg, inv, mode=mode)
    print("---------------")
    if not os.path.exists("llm-generated"):
        os.mkdir("llm-generated")
    output = f"llm-generated/{args.input[args.input.rfind("/"):]}"
    with open(output, "w") as f:
        f.write(inv_prg)
    verified_inv, msg_inv = dafny.verify(output)
    if verified_inv:
        print("Verified with modification")
    else:
        print("Verification failed:")
        print(msg_inv)


if __name__ == '__main__':
    main()
