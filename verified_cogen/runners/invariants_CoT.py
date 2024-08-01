import logging
import re
import textwrap
import json

from verified_cogen.tools.modes import Mode

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner

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
    # logger.info("insert invariants")
    # logger.info(inv)
    # logger.info(prg)
    # logger.info("end invariants")
    return llm.add(prg, inv)


def insert_invariants(llm: LLM, prg: str, inv: str, mode: Mode):
    if mode == Mode.REGEX:
        return insert_invariants_regex(prg, inv)
    elif mode == Mode.LLM:
        return insert_invariants_llm(llm, prg, inv)
    elif mode.is_singlestep:
        raise ValueError("Single-step mode does not require insertion")
    else:
        raise ValueError(f"Unexpected mode: {mode}")


class InvariantCoTRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        response = llm.rewrite(prg)
        try:
            new_prg = json.loads(response)["code"].replace("\\n", "\n")
            logger.info("JSON with invariants: \n {}".format(response))
            logger.info("new_prg : \n {}".format(new_prg))
            return new_prg
        except Exception:
            print("Error parsing response as JSON")
            print(response)
            return prg

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        return llm.produce(prg)

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
