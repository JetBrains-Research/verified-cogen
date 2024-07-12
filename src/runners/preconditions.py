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


class PreconditionRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return llm.rewrite(prg, "preconditions")

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        return llm.produce(prg, "preconditions")

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        if mode == Mode.REGEX:
            raise ValueError("Regex mode not supported for preconditions")
        return llm.add(prg, checks, "preconditions")

    @classmethod
    def precheck(cls, prg: str, mode: Mode):
        fn_count = prg.count("fn")
        if fn_count == 0:
            raise ValueError("No functions in program")

    @classmethod
    def __try_fixing(
        cls,
        logger: Logger,
        verifier: Verifier,
        llm: LLM,
        total_tries: int,
        inv_prg: str,
        name: str,
    ):
        return cls.__try_fixing_inner(
            logger, verifier, llm, total_tries, inv_prg, name, "preconditions"
        )
