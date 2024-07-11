from abc import ABC, abstractmethod
from logging import Logger
from helpers import basename
from llm import LLM
from modes import Mode
from verus import Verus
import os
from typing import Optional


class Runner(ABC):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        """Rewrite the program with additional checks in one step."""
        ...

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        """Produce the additional checks for the program."""
        ...

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        """Insert the additional checks into the program."""
        ...

    @classmethod
    def precheck(cls, prg: str, mode: Mode): ...

    @classmethod
    def __invoke(cls, logger: Logger, llm: LLM, prg: str, mode: Mode) -> str:
        logger.info("Invoking LLM")
        if mode.is_singlestep:
            inv_prg = cls.rewrite(llm, prg)
        else:
            inv = cls.produce(llm, prg)
            inv_prg = cls.insert(llm, prg, inv, mode)
        logger.info("Invocation done")
        return inv_prg

    @classmethod
    def __try_fixing(
        cls,
        logger: Logger,
        verus: Verus,
        llm: LLM,
        total_tries: int,
        inv_prg: str,
        name: str,
    ) -> Optional[int]:
        tries = total_tries
        while tries > 0:
            if not os.path.exists("llm-generated"):
                os.mkdir("llm-generated")
            output = f"llm-generated/{name}"
            with open(output, "w") as f:
                f.write(inv_prg)
            verified_inv, out_inv, err_inv = verus.verify(output)
            if verified_inv:
                return total_tries - tries + 1
            else:
                logger.info("Verification failed:")
                logger.info(out_inv)
                logger.info(err_inv)
                logger.info("Retrying...")
                tries -= 1
                if tries > 0:
                    inv_prg = llm.ask_for_fixed_invariants(err_inv)
        return None

    @classmethod
    def run_on_file(
        cls,
        logger: Logger,
        verus: Verus,
        mode: Mode,
        llm: LLM,
        total_tries: int,
        file: str,
    ) -> Optional[int]:
        logger.info(f"Running on {file}")

        verified, out, err = verus.verify(file)
        if verified:
            return 0

        with open(file, "r") as f:
            prg = f.read()
        cls.precheck(prg, mode)
        inv_prg = cls.__invoke(logger, llm, prg, mode)
        return cls.__try_fixing(
            logger, verus, llm, total_tries, inv_prg, basename(file)
        )
