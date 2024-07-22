from runners import Runner
from verifier import Verifier
from llm import LLM
from modes import Mode
from typing import Optional
import logging
import os
import textwrap
import re
from logging import Logger

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
