import logging
import re
import textwrap

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.tools.modes import Mode

logger = logging.getLogger(__name__)


def insert_invariants_regex(prg: str, inv: str):
    while_loc = prg.find("while")
    assert while_loc > 0
    while_indent = 0
    while (indent := prg[while_loc - while_indent - 1]).isspace():
        if indent == "\t":
            while_indent += 4
        elif indent == " ":
            while_indent += 1
        elif indent == "\n":
            break
        else:
            raise ValueError(f"Unexpected indent before while: {ord(indent)}")
    indented_inv = textwrap.indent(inv, " " * (while_indent + 4))
    return re.sub("while(\\s*\\(.+\\)\\s*)\n", f"while\\1\n{indented_inv}", prg)


def insert_invariants_llm(llm: LLM, prg: str, inv: str):
    return llm.add(prg, inv)


def insert_invariants(llm: LLM, prg: str, inv: str, mode: Mode):
    if mode == Mode.REGEX:
        return insert_invariants_regex(prg, inv)
    elif mode == Mode.LLM:
        return insert_invariants_llm(llm, prg, inv)
    elif mode == Mode.LLM_SINGLE_STEP:
        raise ValueError("Single-step mode does not require insertion")
    else:
        raise ValueError(f"insert_invariants: Unexpected mode: {mode}")


class InvariantRunner(Runner):
    def rewrite(self, prg: str) -> str:
        return self.parser.parse(self.llm.rewrite(prg))

    def produce(self, prg: str) -> str:
        return self.llm.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return insert_invariants(self.llm, prg, checks, mode)

    def precheck(self, prg: str, mode: Mode):
        if mode == Mode.REGEX:
            while_count = prg.count("while")
            if while_count == 0:
                raise ValueError("No loops in program")
            if while_count > 1:
                raise ValueError(
                    "Multiple loops in program, not supported in regex mode"
                )
