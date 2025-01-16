from typing import List, Optional

from verified_cogen.llm import prompts
from verified_cogen.llm.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.runners.languages.language import Language
from verified_cogen.tools.modes import Mode


class ValidatingRunner(Runner):
    wrapped_runner: Runner
    language: Language
    summarizer_llm: LLM
    pure_non_helpers: List[str]

    def __init__(
        self,
        wrapping: Runner,
        language: Language,
    ):
        super().__init__(
            wrapping.llm, wrapping.logger, wrapping.verifier, wrapping.config
        )
        token = wrapping.llm.grazie._grazie_jwt_token  # type: ignore
        self.summarizer_llm = LLM(
            grazie_token=token,
            profile=wrapping.llm.profile.name,
            prompt_dir=wrapping.llm.prompt_dir,
            system_prompt="You are an expert in dafny errors. You will be summarising errors. Don't include the errors you were given\
            in the responses, only summarise them.",
            temperature=0.3,
        )
        self.wrapped_runner = wrapping
        self.language = language
        self.pure_non_helpers = []

    def _add_validators(self, prg: str, inv_prg: str):
        validators = self.language.generate_validators(
            prg, not self.config.remove_helpers
        )
        comment = self.language.simple_comment
        val_prg = inv_prg + "\n" + comment + " ==== verifiers ==== \n" + validators
        return val_prg

    def preprocess(self, prg: str, mode: Mode) -> str:
        if self.config.remove_implementations and not self.config.remove_helpers:
            self.pure_non_helpers = self.language.find_pure_non_helpers(prg)
            self.logger.info(
                "found pure_non_helpers: " + ",".join(self.pure_non_helpers)
            )
        res_prg = self.language.remove_conditions(prg)
        self.wrapped_runner.starting_prg = res_prg
        return res_prg

    def postprocess(self, inv_prg: str) -> str:
        assert self.starting_prg is not None
        if self.config.remove_implementations:
            invalid_helpers: List[str] = []
            try:
                invalid_helpers, inv_prg = self.language.check_helpers(
                    inv_prg, self.pure_non_helpers
                )
                self.logger.info("invalid_helpers: " + ",".join(invalid_helpers))
            except Exception:
                self.logger.info("pass")
                pass
            if invalid_helpers:
                self.llm.add_user_prompt(
                    prompts.invalid_helpers_prompt(self.llm.prompt_dir)
                    .replace("{invalid_helpers}", ",".join(invalid_helpers))
                    .replace("{program}", inv_prg)
                    .replace("{helpers}", ",".join(self.pure_non_helpers))
                )
                self.llm.add_response("understood")
        return self._add_validators(
            self.starting_prg, self.wrapped_runner.postprocess(inv_prg)
        )

    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
        if self.config.remove_implementations:
            additional_prompt += prompts.helpers_prompt(self.llm.prompt_dir).replace(
                "{helpers}", ",".join(self.pure_non_helpers)
            )
        return self.wrapped_runner.rewrite(prg, text_description, additional_prompt)

    def produce(self, prg: str) -> str:
        return self.wrapped_runner.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self.wrapped_runner.insert(prg, checks, mode)

    def ask_for_timeout(self) -> str:
        assert self.starting_prg is not None

        return self.wrapped_runner.ask_for_timeout()

    def ask_for_fixed(self, err: str) -> str:
        assert self.starting_prg is not None

        result, validator = self.language.separate_validator_errors(err)
        if validator:
            self.summarizer_llm.add_user_prompt(
                "Here are the errors you need to summarize:\n" + validator,
            )
            validator_summary = self.summarizer_llm.make_request()
            self.summarizer_llm.user_prompts = []
            self.summarizer_llm.responses = []
            result += (
                "Also, hidden validation errors occurred, here is the summary:\n"
                + validator_summary
            )
        return self.wrapped_runner.ask_for_fixed(result)

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)
