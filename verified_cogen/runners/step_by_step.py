import pathlib
from typing import Optional

from verified_cogen.runners import Runner
from verified_cogen.tools import extract_code_from_llm_output
from verified_cogen.tools.modes import Mode
from verified_cogen.runners.chain_of_thought import Step


class StepByStepConfig:
    remove_old_examples: bool = False

    @classmethod
    def default(cls) -> "StepByStepConfig":
        return cls()


class StepByStepRunner(Runner):
    wrapped_runner: Runner
    config: StepByStepConfig

    def __init__(self, wrapping: Runner, config: Optional[StepByStepConfig] = None):
        super().__init__(wrapping.llm, wrapping.logger, wrapping.verifier)
        self.wrapped_runner = wrapping
        self.config = StepByStepConfig.default() if config is None else config

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.wrapped_runner.preprocess(prg, mode)

    def rewrite(self, prg: str) -> str:
        steps: list[Step] = []
        for step in sorted((pathlib.Path(self.llm.prompt_dir) / "steps").iterdir()):
            assert step.is_dir()
            steps.append(Step(step))
        for step in steps:
            for substep in step.substeps:
                self.llm.add_user_prompt(
                    substep.question, self.config.remove_old_examples
                )
                self.llm.add_response(substep.answer, self.config.remove_old_examples)
            self.llm.add_user_prompt(step.question.replace("{program}", prg))
            _ = self.llm.make_request()
            if self.config.remove_old_examples:
                self.llm.wipe_temporary()

        rewrite_step = Step(pathlib.Path(self.llm.prompt_dir) / "rewrite")
        for substep in rewrite_step.substeps:
            self.llm.add_user_prompt(substep.question, self.config.remove_old_examples)
            self.llm.add_response(substep.answer, self.config.remove_old_examples)
        self.llm.add_user_prompt(rewrite_step.question.replace("{program}", prg))
        response = self.llm.make_request()
        if self.config.remove_old_examples:
            self.llm.wipe_temporary()

        return extract_code_from_llm_output(response)

    def postprocess(self, inv_prg: str) -> str:
        return self.wrapped_runner.postprocess(inv_prg)

    def produce(self, prg: str) -> str:
        return self.wrapped_runner.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self.wrapped_runner.insert(prg, checks, mode)

    def ask_for_timeout(self) -> str:
        return self.wrapped_runner.ask_for_timeout()

    def ask_for_fixed(self, err: str) -> str:
        return self.wrapped_runner.ask_for_fixed(err)

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)
