import logging

from verified_cogen.tools.modes import Mode

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner

logger = logging.getLogger(__name__)


class GenericRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return llm.rewrite(prg)

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        return llm.produce(prg)

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        if mode == Mode.REGEX:
            raise ValueError("Regex mode not supported for generic")
        return llm.add(prg, checks)
