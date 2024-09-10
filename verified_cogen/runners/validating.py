from verified_cogen.runners import Runner
from verified_cogen.runners.languages.language import Language
from verified_cogen.tools.modes import Mode


class ValidatingRunner(Runner):
    wrapped_runner: Runner
    language: Language

    def __init__(self, wrapping: Runner, language: Language):
        super().__init__(wrapping.llm, wrapping.logger, wrapping.verifier)
        self.wrapped_runner = wrapping
        self.language = language

    def _add_validators(self, prg: str, inv_prg: str):
        validators = self.language.generate_validators(prg)
        val_prg = inv_prg + "\n// ==== verifiers ==== //\n" + validators
        return val_prg

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.language.remove_asserts_and_invariants(prg)

    def rewrite(self, prg: str) -> str:
        return self._add_validators(prg, self.wrapped_runner.rewrite(prg))

    def produce(self, prg: str) -> str:
        return self._add_validators(prg, self.wrapped_runner.produce(prg))

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self._add_validators(prg, self.wrapped_runner.insert(prg, checks, mode))

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)
