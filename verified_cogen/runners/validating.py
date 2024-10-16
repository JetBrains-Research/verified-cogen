from typing import Optional

from verified_cogen.llm.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.runners.languages.language import Language
from verified_cogen.tools.modes import Mode


class ValidatingRunner(Runner):
    wrapped_runner: Runner
    language: Language
    summarizer_llm: LLM

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

    def _add_validators(self, prg: str, inv_prg: str):
        validators = self.language.generate_validators(prg)
        comment = self.language.simple_comment
        val_prg = inv_prg + "\n" + comment + " ==== verifiers ==== \n" + validators
        return val_prg

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.language.remove_conditions(prg)

    def postprocess(self, inv_prg: str) -> str:
        assert self.starting_prg is not None
        return self._add_validators(
            self.starting_prg, self.wrapped_runner.postprocess(inv_prg)
        )

    def rewrite(self, prg: str, text_description: Optional[str] = None) -> str:
        return self.wrapped_runner.rewrite(prg, text_description)

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
                "Also, hidden validation errors occured, here is the summary:\n"
                + validator_summary
            )
        return self.wrapped_runner.ask_for_fixed(result)

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)
