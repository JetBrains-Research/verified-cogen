import logging

from verified_cogen.tools.modes import Mode

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner

logger = logging.getLogger(__name__)


class GenericRunner(Runner):
    def rewrite(self, prg: str) -> str:
        return self.llm.rewrite(prg)

    def produce(self, prg: str) -> str:
        return self.llm.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        if mode == Mode.REGEX:
            raise ValueError("Regex mode not supported for generic")
        return self.llm.add(prg, checks)
