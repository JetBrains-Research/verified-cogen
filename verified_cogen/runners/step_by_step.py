import pathlib

from verified_cogen.runners import Runner
from verified_cogen.tools.modes import Mode
from verified_cogen.runners.chain_of_thought import Step


class StepByStepRunner(Runner):
    wrapped_runner: Runner

    def __init__(self, wrapping: Runner):
        super().__init__(wrapping.llm, wrapping.logger, wrapping.verifier)
        self.wrapped_runner = wrapping

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.wrapped_runner.preprocess(prg, mode)

    def rewrite(self, prg: str) -> str:
        steps: list[Step] = []
        for step in sorted((pathlib.Path(self.llm.prompt_dir) / "steps").iterdir()):
            assert step.is_dir()
            steps.append(Step(step))
        for step in steps:
            for substep in step.substeps:
                self.llm.add_user_prompt(substep.question)
                self.llm.add_response(substep.answer)
            self.llm.add_user_prompt(step.question.replace("{program}", prg))
            _ = self.llm.make_request()
        return self.wrapped_runner.rewrite(prg)

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
