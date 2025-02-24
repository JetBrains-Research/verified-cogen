from typing import Optional

from verified_cogen.config import LLMConfig


class Rewriter:
    llm_with_idx: Optional[tuple[LLMConfig, int]]

    def __init__(self, llm: Optional[tuple[LLMConfig, int]] = None):
        self.llm_with_idx = llm

    def rewrite(self, prg: str, error: Optional[str] = None) -> tuple[str, str]: ...
