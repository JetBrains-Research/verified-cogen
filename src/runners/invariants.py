from runners import Runner
from verifier import Verifier
from llm import LLM
from modes import Mode
from typing import Optional
import logging
import os
import textwrap
import re

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


def insert_invariants_llm(llm: LLM, prg, inv):
    return llm.add(prg, inv, "invariants")


def insert_invariants(llm: LLM, prg: str, inv: str, mode: Mode):
    if mode == Mode.REGEX:
        return insert_invariants_regex(prg, inv)
    elif mode == Mode.LLM:
        return insert_invariants_llm(llm, prg, inv)
    elif mode.is_singlestep:
        raise ValueError("Single-step mode does not require insertion")
    else:
        raise ValueError(f"Unexpected mode: {mode}")


class InvariantRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return llm.rewrite(prg, "invariants")

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        return llm.produce(prg, "invariants")

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        return insert_invariants(llm, prg, checks, mode)

    @classmethod
    def precheck(cls, prg: str, mode: Mode):
        while_count = prg.count("while")
        if while_count == 0:
            raise ValueError("No loops in program")
        if mode == Mode.REGEX:
            if while_count > 1:
                raise ValueError(
                    "Multiple loops in program, not supported in regex mode"
                )
