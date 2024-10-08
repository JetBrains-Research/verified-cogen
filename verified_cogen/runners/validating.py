import pathlib
from typing import Optional
from verified_cogen.runners import Runner
from verified_cogen.runners.languages.language import Language
from verified_cogen.tools.modes import Mode


class ValidatingRunner(Runner):
    wrapped_runner: Runner
    language: Language

    def __init__(
        self,
        wrapping: Runner,
        language: Language,
        log_tries: Optional[pathlib.Path] = None,
    ):
        super().__init__(wrapping.llm, wrapping.logger, wrapping.verifier, log_tries)
        self.wrapped_runner = wrapping
        self.language = language

    def _add_validators(self, prg: str, inv_prg: str):
        validators = self.language.generate_validators(prg)
        comment = self.language.simple_comment
        val_prg = inv_prg + "\n" + comment + " ==== verifiers ==== \n" + validators
        return val_prg

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.language.remove_asserts_and_invariants(prg)

    def postprocess(self, inv_prg: str) -> str:
        assert self.starting_prg is not None
        return self._add_validators(
            self.starting_prg, self.wrapped_runner.postprocess(inv_prg)
        )

    def rewrite(self, prg: str) -> str:
        return self.wrapped_runner.rewrite(prg)

    def produce(self, prg: str) -> str:
        return self.wrapped_runner.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self.wrapped_runner.insert(prg, checks, mode)

    def ask_for_timeout(self) -> str:
        assert (
            self.starting_prg is not None
        ), "one of: rewrite, produce, insert must be called before ask_for_timeout"
        return self.wrapped_runner.ask_for_timeout()

    def ask_for_fixed(self, err: str) -> str:
        assert (
            self.starting_prg is not None
        ), "one of: rewrite, produce, insert must be called before ask_for_fixed"
        return self.wrapped_runner.ask_for_fixed(err)

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)
