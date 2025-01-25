from typing import Optional

from verified_cogen.runners import Runner
from verified_cogen.tools import compare_errors
from verified_cogen.tools.modes import Mode


class FlushRunner(Runner):
    previous_error: str = ""
    timeout: str = "Verification timed out"

    wrapped_runner: Runner

    def __init__(self, wrapped_runner: Runner):
        super().__init__(
            wrapped_runner.llm,
            wrapped_runner.logger,
            wrapped_runner.verifier,
            wrapped_runner.config,
        )
        self.wrapped_runner = wrapped_runner

    def flush_and_rewrite(self) -> str:
        assert self.starting_prg is not None
        self.llm.wipe_all()
        self.previous_error = ""
        self.logger.info(
            f"Encountered same error for {self.wrapped_runner.get_name()}. Rewrite"
        )
        return self.rewrite(self.starting_prg)

    def ask_for_timeout(self) -> str:
        if compare_errors(self.previous_error, self.timeout):
            return self.flush_and_rewrite()
        else:
            self.previous_error = self.timeout
            return self.wrapped_runner.ask_for_timeout()

    def ask_for_fixed(self, err: str) -> str:
        if compare_errors(self.previous_error, err):
            return self.flush_and_rewrite()
        else:
            self.previous_error = err
            return self.wrapped_runner.ask_for_fixed(err)

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.wrapped_runner.preprocess(prg, mode)

    def postprocess(self, inv_prg: str) -> str:
        return self.wrapped_runner.postprocess(inv_prg)

    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
        return self.wrapped_runner.rewrite(prg, text_description, additional_prompt)

    def produce(self, prg: str) -> str:
        return self.wrapped_runner.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self.wrapped_runner.insert(prg, checks, mode)

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)
