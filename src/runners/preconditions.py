from runners import Runner
from verus import Verus
from llm import LLM
from modes import Mode
from typing import Optional
import logging
import os
import textwrap
import re

logger = logging.getLogger(__name__)


class PreconditionRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return llm.rewrite_with_preconditions(prg)

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        return llm.produce_preconditions(prg)

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        return llm.add_preconditions(prg, checks)

    @classmethod
    def precheck(cls, prg: str, mode: Mode):
        fn_count = prg.count("fn")
        if fn_count == 0:
            raise ValueError("No functions in program")
