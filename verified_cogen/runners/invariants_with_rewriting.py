from logging import Logger
from typing import Optional

from verified_cogen.llm import LLM
from verified_cogen.runners import RunnerConfig
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.tools import rewrite_error
from verified_cogen.tools.verifier import Verifier


class InvariantsWithRewriting(InvariantRunner):
    rewriter: Rewriter
    previous_prg: Optional[str] = None

    def __init__(
        self,
        llm: LLM,
        logger: Logger,
        verifier: Verifier,
        config: RunnerConfig,
        rewriter: Rewriter,
    ):
        super().__init__(llm, logger, verifier, config)
        self.rewriter = rewriter

    def postprocess(self, inv_prg: str) -> str:
        prg, prompt = self.rewriter.rewrite(inv_prg)

        if prompt != "":
            self.logger.info("Manually rewrite:")
            self.logger.info(inv_prg)
            self.logger.info("Manual rewriting results:")
            self.logger.info(prompt)
            self.llm.add_user_prompt(prompt)

        self.previous_prg = prg

        return prg

    def ask_for_fixed(self, err: str) -> str:
        assert self.previous_prg is not None
        modified_err = rewrite_error(self.previous_prg, err)
        return super().ask_for_fixed(modified_err)
