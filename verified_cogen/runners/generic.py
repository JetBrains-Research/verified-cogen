import logging

from typing_extensions import Optional

from verified_cogen.runners import Runner
from verified_cogen.tools.modes import Mode

logger = logging.getLogger(__name__)


class GenericRunner(Runner):
    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
        return self.llm.rewrite(prg, text_description, additional_prompt)

    def produce(self, prg: str) -> str:
        return self.llm.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        if mode == Mode.REGEX:
            raise ValueError("Regex mode not supported for generic")
        return self.llm.add(prg, checks)
