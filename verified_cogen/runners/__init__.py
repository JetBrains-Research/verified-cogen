import pathlib
from logging import Logger
from typing import Optional

from verified_cogen.llm import LLM
from verified_cogen.tools import basename, get_cache_dir
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

LLM_GENERATED_DIR = pathlib.Path(get_cache_dir()) / "llm-generated"


class Runner:
    llm: LLM
    logger: Logger
    verifier: Verifier
    log_tries: Optional[pathlib.Path]
    starting_prg: Optional[str] = None

    def __init__(
        self,
        llm: LLM,
        logger: Logger,
        verifier: Verifier,
        log_tries: Optional[pathlib.Path] = None,
    ):
        self.llm = llm
        self.logger = logger
        self.verifier = verifier
        self.log_tries = log_tries
        if self.log_tries is not None:
            self.log_tries.mkdir(exist_ok=True, parents=True)

    def rewrite(self, prg: str) -> str:
        """Rewrite the program with additional checks in one step."""
        ...

    def produce(self, prg: str) -> str:
        """Produce the additional checks for the program."""
        ...

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        """Insert the additional checks into the program."""
        ...

    def ask_for_timeout(self) -> str:
        """Ask the LLM to fix the program with a timeout."""
        return self.llm.ask_for_timeout()

    def ask_for_fixed(self, err: str) -> str:
        """Ask the LLM to fix the program with the given output."""
        return self.llm.ask_for_fixed(err)

    def precheck(self, prg: str, mode: Mode):
        pass

    def preprocess(self, prg: str, mode: Mode) -> str:
        return prg

    def postprocess(self, inv_prg: str) -> str:
        return inv_prg

    def invoke(self, prg: str, mode: Mode) -> str:
        self.logger.info("Invoking LLM")
        if mode == Mode.LLM_SINGLE_STEP:
            inv_prg = self.rewrite(prg)
        elif mode == Mode.LLM or mode == Mode.REGEX:
            checks = self.produce(prg)
            inv_prg = self.insert(prg, checks, mode)
        else:
            raise ValueError(f"Unexpected mode: {mode}")
        self.logger.info("Invocation done")
        return inv_prg

    def _verification_file(self, name: str, try_n: int) -> pathlib.Path:
        if self.log_tries is not None:
            base, extension = name.rsplit(".", 1)
            return self.log_tries / f"{base}.{try_n}.{extension}"
        else:
            return LLM_GENERATED_DIR / name

    def verify_program(self, name: str, try_n: int, prg: str):
        LLM_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        output = self._verification_file(name, try_n)
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
            verification_result = self.verify_program(
                name, total_tries - tries + 1, inv_prg
            )
            if verification_result is None:
                self.logger.info("Verification timed out")
                tries -= 1
                if tries > 0:
                    inv_prg = self.postprocess(self.ask_for_timeout())
            else:
                verified_inv, out_inv, err_inv = verification_result
                if verified_inv:
                    return total_tries - tries + 1
                else:
                    self.logger.info("Verification failed:")
                    self.logger.info(out_inv)
                    self.logger.info(err_inv)
                    tries -= 1
                    if tries > 0:
                        self.logger.info(f"Retrying with {tries} tries left...")
                        inv_prg = self.postprocess(
                            self.ask_for_fixed(out_inv + err_inv)
                        )
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

        self.starting_prg = prg

        verification_result = self.verify_program(name, 0, self.postprocess(prg))
        if verification_result is not None and verification_result[0]:
            return 0
        elif verification_result is None:
            self.logger.info("Verification timed out")
        self.precheck(prg, mode)
        inv_prg = self.postprocess(self.invoke(prg, mode))
        return self.try_fixing(total_tries, inv_prg, name)
