import logging
import re
import textwrap
import pathlib

from typing import Optional

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.runners.config import Config
from verified_cogen.tools.modes import Mode
from verified_cogen.tools import basename
from verified_cogen.tools.verifier import Verifier
from verified_cogen.experiments import houdini
from verified_cogen.llm import prompts


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
    elif mode.is_singlestep:
        raise ValueError("Single-step mode does not require insertion")
    else:
        raise ValueError(f"Unexpected mode: {mode}")


class InvariantRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return llm.rewrite(prg)

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

    @classmethod
    def run_on_file(
        cls,
        logger: logging.Logger,
        verifier: Verifier,
        mode: Mode,
        llm: LLM,
        total_tries: int,
        file: str,
        config: Config,
    ) -> Optional[int]:
        if config.with_houdini:
            with open(file, "r") as f:
                prg = f.read()
            cls.precheck(prg, mode)

            verification_result = verifier.verify(pathlib.Path(file))
            if verification_result is not None and verification_result[0]:
                return 0
            elif verification_result is None:
                logger.info("Verification timed out")

            houdini_run = houdini.run_on(
                llm, verifier, prg, basename(file), llm.grazie_token, llm.prompt_dir
            )

            if houdini_run is not None:
                return -1

            llm.reset()
            llm.set_system_prompt(prompts.sys_prompt(llm.prompt_dir))

        return cls.generic_run_on_file(logger, verifier, mode, llm, total_tries, file)
