from typing import Optional
from verified_cogen.runners import Runner
from verified_cogen.runners.step_by_step import StepByStepRunner, StepByStepConfig
from verified_cogen.tools import compare_errors


class StepByStepFlushRunner(StepByStepRunner):
    previous_error: str = ""
    timeout: str = "Verification timed out"

    def __init__(self, wrapping: Runner, config: Optional[StepByStepConfig] = None):
        super().__init__(wrapping, config)

    def flush_and_rewrite(self) -> str:
        assert self.starting_prg is not None
        self.llm.wipe_all()
        self.previous_error = ""
        self.logger.info("Encountered same error. Rewrite")
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
