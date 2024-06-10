from dafny import Dafny
from llm.llm import LLM
import textwrap
import argparse
import os
import re

def precheck(prg):
    while_count = prg.count("while")
    if while_count == 0:
        print("No loops in program")
        return False
    if while_count > 1:
        print("Multiple loops in program, TODO")
        return False
    return True


def insert_invariants(prg, inv):
    while_loc = prg.find("while")
    assert while_loc > 0
    while_indent = 0
    while (indent := prg[while_loc - while_indent - 1]).isspace():
        if indent == '\t':
            while_indent += 4
        elif indent == ' ':
            while_indent += 1
        elif indent == '\n':
            break
        else:
            raise ValueError(f"Unexpected indent before while: {ord(indent)}")
    indented_inv = textwrap.indent(inv, ' ' * (while_indent + 4))
    return re.sub("while(\\s*\\(.+\\)\\s*)\n", f"while\\1\n{indented_inv}", prg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("--dafny-path", help="dafny path", default="dafny")
    parser.add_argument("--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN"))
    args = parser.parse_args()
    if args.input is None:
        args.input = input("Input file: ")
    dafny = Dafny(args.dafny_path)
    verified, msg = dafny.verify(args.input)
    if verified:
        print("Verified without modification")
        return
    with open(args.input, "r") as f:
        prg = f.read()
    if not precheck(prg):
        return
    print("---------------")

    llm = LLM(args.grazie_token)
    inv = llm.produce_invariants(prg).content
    print("Adding invariants:")
    print(inv)
    print("---------------")
    if not os.path.exists("llm-generated"):
        os.mkdir("llm-generated")
    output = f"llm-generated/{args.input[args.input.rfind("/"):]}"
    with open(output, "w") as f:
        f.write(insert_invariants(prg, inv))
    verified_inv, msg_inv = dafny.verify(output)
    if verified_inv:
        print("Verified with modification")
    else:
        print("Verification failed:")
        print(msg_inv)


if __name__ == '__main__':
    main()
