import logging
import re
import textwrap

from typing_extensions import Optional

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner, RunnerConfig
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

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
    rewriter: Optional[Rewriter]
    previous_prg: Optional[str] = None

    def __init__(
        self,
        llm: LLM,
        logger: logging.Logger,
        verifier: Verifier,
        config: RunnerConfig,
        rewriter: Optional[Rewriter] = None,
    ):
        super().__init__(llm, logger, verifier, config)
        self.rewriter = rewriter

    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
        return self.llm.rewrite(prg, text_description, additional_prompt)

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

    def postprocess(self, inv_prg: str) -> str:
        if self.rewriter is not None:
            prg, prompt = self.rewriter.rewrite(inv_prg)

            if prompt != "":
                self.logger.info("Manually rewrite:")
                self.logger.info(inv_prg)
                self.logger.info("Manual rewriting results:")
                self.logger.info(prompt)
                self.llm.add_user_prompt(prompt)
                self.llm.add_response("understood")
        else:
            prg = super().postprocess(inv_prg)

        self.previous_prg = prg

        return prg
