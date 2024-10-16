import pathlib
from typing import Optional

from verified_cogen.runners import Runner
from verified_cogen.runners.chain_of_thought.step import Step, Substep
from verified_cogen.tools import extract_code_from_llm_output
from verified_cogen.tools.modes import Mode


class StepByStepConfig:
    remove_old_examples: bool = False
    full_examples: bool = True

    @classmethod
    def default(cls) -> "StepByStepConfig":
        return cls()


class StepByStepRunner(Runner):
    wrapped_runner: Runner
    _config: StepByStepConfig

    def __init__(self, wrapping: Runner, config: Optional[StepByStepConfig] = None):
        super().__init__(
            wrapping.llm, wrapping.logger, wrapping.verifier, wrapping.config
        )
        self.wrapped_runner = wrapping
        self._config = StepByStepConfig.default() if config is None else config

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.wrapped_runner.preprocess(prg, mode)

    def rewrite(self, prg: str, text_description: Optional[str] = None) -> str:
        return (
            self.rewrite_full_examples(prg, text_description)
            if self._config.full_examples
            else self.rewrite_step_by_step(prg, text_description)
        )

    def _make_rewrite_prompt(
        self, template: str, program: str, text_description: Optional[str]
    ) -> str:
        result = template.replace("{program}", program)
        if text_description is not None and "{text_description}" in result:
            result = result.replace("{text_description}", text_description)
        return result

    def rewrite_step_by_step(self, prg: str, text_description: Optional[str]) -> str:
        def add_examples(step: Step):
            for sub_step in step.examples:
                self.llm.add_user_prompt(
                    sub_step.question, self._config.remove_old_examples
                )
                self.llm.add_response(sub_step.answer, self._config.remove_old_examples)

        steps: list[Step] = []
        for step in sorted((pathlib.Path(self.llm.prompt_dir) / "steps").iterdir()):
            assert step.is_dir()
            steps.append(Step(step))
        for it, step in enumerate(steps):
            add_examples(step)
            self.llm.add_user_prompt(
                self._make_rewrite_prompt(step.question, prg, text_description)
            )
            _ = self.llm.make_request()
            if self._config.remove_old_examples:
                self.llm.wipe_temporary()
            self.logger.info(f"Step {it + 1} done")

        rewrite_step = Step(pathlib.Path(self.llm.prompt_dir) / "rewrite")
        add_examples(rewrite_step)
        self.llm.add_user_prompt(
            self._make_rewrite_prompt(rewrite_step.question, prg, text_description)
        )
        response = self.llm.make_request()
        if self._config.remove_old_examples:
            self.llm.wipe_temporary()

        return extract_code_from_llm_output(response)

    def rewrite_full_examples(self, prg: str, text_description: Optional[str]) -> str:
        steps: list[Step] = []
        for step in sorted((pathlib.Path(self.llm.prompt_dir) / "steps").iterdir()):
            assert step.is_dir()
            steps.append(Step(step))

        assert all(len(step.examples) == len(steps[0].examples) for step in steps)

        rewrite_step = Step(pathlib.Path(self.llm.prompt_dir) / "rewrite")
        assert len(steps) == 0 or len(rewrite_step.examples) == len(steps[0].examples)

        examples: list[list[Substep]] = list(
            zip(*([step.examples for step in steps] + [rewrite_step.examples]))
        )

        for example in examples:
            for sub_step in example:
                self.llm.add_user_prompt(sub_step.question)
                self.llm.add_response(sub_step.answer)

        for it, step in enumerate(steps):
            self.llm.add_user_prompt(
                self._make_rewrite_prompt(step.question, prg, text_description)
            )
            _ = self.llm.make_request()
            self.logger.info(f"Step {it + 1} done")

        self.llm.add_user_prompt(
            self._make_rewrite_prompt(rewrite_step.question, prg, text_description)
        )
        response = self.llm.make_request()

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
