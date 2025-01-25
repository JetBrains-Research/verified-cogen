import pathlib
from logging import Logger
from pathlib import Path
from typing import Optional

from verified_cogen.llm import LLM
from verified_cogen.tools import basename, get_cache_dir
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

LLM_GENERATED_DIR = pathlib.Path(get_cache_dir()) / "llm-generated"


class RunnerConfig:
    log_tries: Optional[pathlib.Path] = None
    include_text_descriptions: bool = False
    remove_implementations: bool = False
    remove_helpers: bool = False

    def __init__(
        self,
        log_tries: Optional[pathlib.Path] = None,
        include_text_descriptions: bool = False,
        remove_implementations: bool = False,
        remove_helpers: bool = False,
    ):
        self.log_tries = log_tries
        self.include_text_descriptions = include_text_descriptions
        self.remove_implementations = remove_implementations
        self.remove_helpers = remove_helpers


class Runner:
    llm: LLM
    logger: Logger
    verifier: Verifier
    starting_prg: Optional[str] = None
    name: Optional[str] = None
    config: RunnerConfig

    def __init__(
        self, llm: LLM, logger: Logger, verifier: Verifier, config: RunnerConfig
    ):
        self.llm = llm
        self.logger = logger
        self.verifier = verifier
        self.config = config
        if self.config.log_tries is not None:
            self.config.log_tries.mkdir(exist_ok=True, parents=True)

    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
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

    def get_name(self) -> str:
        return self.name or "unknown"

    def invoke(
        self, prg: str, mode: Mode, text_description: Optional[str] = None
    ) -> str:
        self.logger.info(f"Invoking LLM for {self.get_name()}")
        if mode == Mode.LLM_SINGLE_STEP:
            inv_prg = self.rewrite(prg, text_description)
        elif mode == Mode.LLM or mode == Mode.REGEX:
            checks = self.produce(prg)
            inv_prg = self.insert(prg, checks, mode)
        else:
            raise ValueError(f"Unexpected mode: {mode} for {self.get_name()}")
        self.logger.info(f"Invocation done for {self.get_name()}")
        return inv_prg

    def _verification_file(self, name: str, try_n: int) -> pathlib.Path:
        if self.config.log_tries is not None:
            base, extension = name.rsplit(".", 1)
            return self.config.log_tries / f"{base}_{try_n}.{extension}"
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
                self.logger.info(f"Verification timed out for {self.get_name()}")
                tries -= 1
                if tries > 0:
                    inv_prg = self.postprocess(self.ask_for_timeout())
            else:
                verified_inv, out_inv, err_inv = verification_result
                if verified_inv:
                    return total_tries - tries + 1
                else:
                    self.logger.info(f"Verification failed for {self.get_name()}:")
                    self.logger.info(out_inv)
                    self.logger.info(err_inv)
                    tries -= 1
                    if tries > 0:
                        self.logger.info(
                            f"Retrying {self.get_name()} with {tries} tries left..."
                        )
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

        file_path = Path(file)
        with file_path.open() as f:
            prg = f.read()

        text_description = None
        if self.config.include_text_descriptions:
            text_description_file = (
                file_path.parent / "text-descriptions" / f"{file_path.stem}.txt"
            )
            text_description = text_description_file.read_text()
            self.logger.info(f"Text description for {name}: {text_description}")

        self.starting_prg = prg
        self.name = name
        prg = self.preprocess(prg, mode)

        verification_result = self.verify_program(name, 0, self.postprocess(prg))
        if verification_result is not None and verification_result[0]:
            return 0
        elif verification_result is None:
            self.logger.info(f"Verification timed out for {name}")
        self.precheck(prg, mode)
        inv_prg = self.postprocess(self.invoke(prg, mode, text_description))
        return self.try_fixing(total_tries, inv_prg, name)
