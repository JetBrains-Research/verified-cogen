import logging
import pathlib
from typing import Optional

from verified_cogen.runners import Runner
from verified_cogen.tools import basename, get_cache_dir
from verified_cogen.tools.modes import Mode

LLM_GENERATED_DIR = pathlib.Path(get_cache_dir()) / "llm-generated"

logger = logging.getLogger(__name__)


class GenerateRunner(Runner):
    def rewrite(self, prg: str, text_description: Optional[str] = None) -> str:
        return self.llm.rewrite(prg)

    def produce(self, prg: str) -> str:
        raise ValueError("Produce not supported for generate")

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        raise ValueError("Insert not supported for generate")

    def try_fixing(
        self,
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
            verification_result = self.verifier.verify(output)
            if verification_result is None:
                logger.info("Verification timed out")
                tries -= 1
                if tries > 0:
                    inv_prg = self.llm.ask_for_timeout()
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
                        inv_prg = self.llm.ask_for_fixed(out_inv + err_inv)
        return None

    def run_on_file(
        self,
        mode: Mode,
        total_tries: int,
        file: str,
    ) -> Optional[int]:
        logger.info(f"Running on {file}")

        with open(file, "r") as f:
            prg = f.read()
        self.precheck(prg, mode)
        inv_prg = self.invoke(prg, mode)
        return self.try_fixing(total_tries, inv_prg, basename(file))
