from logging import Logger
from typing import Optional
import pathlib

from verified_cogen.tools import basename, get_cache_dir
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier
from verified_cogen.llm import LLM

LLM_GENERATED_DIR = pathlib.Path(get_cache_dir()) / "llm-generated"


class Runner:
    llm: LLM
    logger: Logger
    verifier: Verifier

    def __init__(self, llm: LLM, logger: Logger, verifier: Verifier):
        self.llm = llm
        self.logger = logger
        self.verifier = verifier

    def rewrite(self, prg: str) -> str:
        """Rewrite the program with additional checks in one step."""
        ...

    def produce(self, prg: str) -> str:
        """Produce the additional checks for the program."""
        ...

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        """Insert the additional checks into the program."""
        ...

    def precheck(self, prg: str, mode: Mode):
        pass

    def preprocess(self, prg: str, mode: Mode) -> str:
        return prg

    def invoke(self, prg: str, mode: Mode) -> str:
        self.logger.info("Invoking LLM")
        if mode.is_singlestep:
            inv_prg = self.rewrite(prg)
        else:
            raise ValueError(f"Unexpected mode: {mode}")
        self.logger.info("Invocation done")
        return inv_prg

    def verify_program(self, name: str, prg: str):
        LLM_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        output = LLM_GENERATED_DIR / name
        with open(output, "w") as f:
            f.write(prg)
        return self.verifier.verify(output)

    def try_fixing(
        self,
        total_tries: int,
        inv_prg: str,
        name: str,
    ) -> Optional[int]:
        tries = total_tries
        while tries > 0:
            verification_result = self.verify_program(name, inv_prg)
            if verification_result is None:
                self.logger.info("Verification timed out")
                tries -= 1
                if tries > 0:
                    inv_prg = self.llm.ask_for_timeout()
            else:
                verified_inv, out_inv, err_inv = verification_result
                if verified_inv:
                    return total_tries - tries + 1
                else:
                    self.logger.info("Verification failed:")
                    self.logger.info(out_inv)
                    self.logger.info(err_inv)
                    self.logger.info("Retrying...")
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
        name = basename(file)
        self.logger.info(f"Running on {file}")

        with open(file, "r") as f:
            prg = self.preprocess(f.read(), mode)

        verification_result = self.verify_program(name, prg)
        if verification_result is not None and verification_result[0]:
            return 0
        elif verification_result is None:
            self.logger.info("Verification timed out")
        self.precheck(prg, mode)
        inv_prg = self.invoke(prg, mode)
        return self.try_fixing(total_tries, inv_prg, name)
