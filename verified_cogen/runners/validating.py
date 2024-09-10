import re
from logging import Logger

from verified_cogen.runners.languages.language import Language
from verified_cogen.tools.modes import Mode

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.tools.verifier import Verifier


class ValidatingRunner(Runner):
    invariant_runner: InvariantRunner
    language: Language

    def __init__(
        self, llm: LLM, logger: Logger, verifier: Verifier, language: Language
    ):
        super().__init__(llm, logger, verifier)
        self.invariant_runner = InvariantRunner(llm, logger, verifier)
        self.language = language

    def _add_validators(self, prg: str, inv_prg: str):
        validators = self.language.generate_validators(prg)
        val_prg = inv_prg + "\n// ==== verifiers ==== //\n" + validators
        return val_prg

    def preprocess(self, prg: str, mode: Mode) -> str:
        return self.language.remove_asserts_and_invariants(prg)

    def rewrite(self, prg: str) -> str:
        return self._add_validators(prg, self.invariant_runner.rewrite(prg))

    def produce(self, prg: str) -> str:
        return self._add_validators(prg, self.invariant_runner.produce(prg))

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self._add_validators(
            prg, self.invariant_runner.insert(prg, checks, mode)
        )

    def precheck(self, prg: str, mode: Mode):
        return self.invariant_runner.precheck(prg, mode)
