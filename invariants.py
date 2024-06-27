import re
import textwrap
from modes import Modes


def insert_invariants_regex(prg, inv):
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


def insert_invariants_llm(llm, prg, inv):
    return llm.add_invariants(prg, inv)


def insert_invariants(dafny, llm, prg, inv, *, mode):
    if mode == Modes.REGEX:
        return insert_invariants_regex(prg, inv)
    elif mode == Modes.LLM:
        return insert_invariants_llm(llm, prg, inv)
    elif mode.is_singlestep:
        raise ValueError("Single-step mode does not require insertion")
    else:
        raise ValueError(f"Unexpected mode: {mode}")