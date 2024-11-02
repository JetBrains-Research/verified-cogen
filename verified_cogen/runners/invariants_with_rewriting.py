from logging import Logger

from verified_cogen.llm import LLM
from verified_cogen.runners import RunnerConfig
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.tools.verifier import Verifier


class InvariantsWithRewriting(InvariantRunner):
    rewriter: Rewriter

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
            self.logger.info("Manual rewriting results: ")
            self.logger.info(prompt)
            self.llm.add_user_prompt(prompt)

        return prg
