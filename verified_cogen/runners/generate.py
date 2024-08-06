import logging
from typing import Optional
import pathlib

from verified_cogen.tools.modes import Mode

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.tools.verifier import Verifier
from verified_cogen.tools import basename, get_cache_dir


LLM_GENERATED_DIR = pathlib.Path(get_cache_dir()) / "llm-generated"

logger = logging.getLogger(__name__)


class GenerateRunner(Runner):
    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return llm.rewrite(prg)

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        raise ValueError("Produce not supported for generate")

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        raise ValueError("Insert not supported for generate")

    @classmethod
    def try_fixing(
        cls,
        logger: logging.Logger,
        verifier: Verifier,
        llm: LLM,
        total_tries: int,
        inv_prg: str,
        name: str,
    ) -> Optional[int]:
        tries = total_tries
        while tries > 0:
            LLM_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
            output = LLM_GENERATED_DIR / f"{name[:-7]}.dfy"
            with open(output, "w") as f:
                f.write(inv_prg)
            verification_result = verifier.verify(output)
            if verification_result is None:
                logger.info("Verification timed out")
                tries -= 1
                if tries > 0:
                    inv_prg = llm.ask_for_timeout()
            else:
                verified_inv, out_inv, err_inv = verification_result
                if verified_inv:
                    return total_tries - tries + 1
                else:
                    logger.info("Verification failed:")
                    logger.info(out_inv)
                    logger.info(err_inv)
                    logger.info("Retrying...")
                    tries -= 1
                    if tries > 0:
                        inv_prg = llm.ask_for_fixed(out_inv + err_inv)
        return None

    @classmethod
    def run_on_file(
        cls,
        logger: logging.Logger,
        verifier: Verifier,
        mode: Mode,
        llm: LLM,
        total_tries: int,
        file: str,
    ) -> Optional[int]:
        logger.info(f"Running on {file}")

        with open(file, "r") as f:
            prg = f.read()
        cls.precheck(prg, mode)
        inv_prg = cls.invoke(logger, llm, prg, mode)
        return cls.try_fixing(
            logger, verifier, llm, total_tries, inv_prg, basename(file)
        )
