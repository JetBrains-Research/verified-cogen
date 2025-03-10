import json
import pathlib
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Optional

from verified_cogen.llm import LLM
from verified_cogen.tools import basename as basename
from verified_cogen.tools import get_cache_dir
from verified_cogen.tools.modes import Mode
from verified_cogen.tools.verifier import Verifier

LLM_GENERATED_DIR = pathlib.Path(get_cache_dir()) / "llm-generated"


@dataclass
class RunnerConfig:
    log_tries: Optional[pathlib.Path] = None
    include_text_descriptions: bool = False
    run_tests: bool = False
    remove_implementations: bool = False
    remove_helpers: bool = False

    def __init__(
        self,
        log_tries: Optional[pathlib.Path] = None,
        include_text_descriptions: bool = False,
        remove_implementations: bool = False,
        remove_helpers: bool = False,
        record_history: bool = False,
    ):
        self.log_tries = log_tries
        self.include_text_descriptions = include_text_descriptions
        self.remove_implementations = remove_implementations
        self.remove_helpers = remove_helpers
        self.record_history = record_history


class Runner:
    llm: LLM
    logger: Logger
    verifier: Verifier
    starting_prg: Optional[str] = None
    name: Optional[str] = None
    test_description: Optional[str] = None
    tests: Optional[str] = None
    config: RunnerConfig
    history: dict[str, tuple[bool, str, str]]

    def __init__(self, llm: LLM, logger: Logger, verifier: Verifier, config: RunnerConfig):
        self.llm = llm
        self.logger = logger
        self.verifier = verifier
        self.config = config
        if self.config.log_tries is not None:
            self.config.log_tries.mkdir(exist_ok=True, parents=True)
        self.history = {}

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

    def invoke(self, prg: str, mode: Mode, text_description: Optional[str] = None) -> str:
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

    @staticmethod
    def combine_name(name: str, try_n: int, tag: str = "") -> str:
        base, extension = name.rsplit(".", 1)
        return f"{base}{tag}_{try_n}.{extension}"

    def _base_dir(self):
        if self.config.log_tries is not None:
            return self.config.log_tries
        else:
            return LLM_GENERATED_DIR

    def _verification_file(self, name: str, try_n: int, tag: str = "") -> pathlib.Path:
        if self.config.log_tries is not None:
            return self.config.log_tries / Runner.combine_name(name, try_n, tag)
        else:
            return LLM_GENERATED_DIR / name

    def verify_program(self, name: str, try_n: int, prg: str, tag: str = ""):
        LLM_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        output = self._verification_file(name, try_n, tag)
        with open(output, "w") as f:
            f.write(prg)
        res = self.verifier.verify(output)
        if self.config.record_history and res is not None:
            self.history[Runner.combine_name(name, try_n, tag)] = res
        return res

    def test_program(self, name: str, try_n: int, prg: str, tag: str = ""):
        full_name = Runner.combine_name(name, try_n, tag)
        working_dir = self._base_dir() / full_name.rsplit(".", 1)[0]
        working_dir.mkdir(parents=True, exist_ok=True)
        output = working_dir / full_name
        with open(output, "w") as f:
            f.write(prg)
        res = self.verifier.test(output)
        if self.config.record_history and res is not None:
            self.history[full_name] = res
        return res

    def get_history(self):
        return self.history

    def dump_history(self, file: Path):
        with open(file, "w") as f:
            json.dump({k: res for k, (res, _, _) in self.get_history().items()}, f)

    def try_fixing(
        self,
        total_tries: int,
        inv_prg: str,
        name: str,
    ) -> Optional[int]:
        tries = total_tries
        while tries > 0:
            verification_result = self.verify_program(name, total_tries - tries + 1, inv_prg)
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
                        self.logger.info(f"Retrying {self.get_name()} with {tries} tries left...")
                        inv_prg = self.postprocess(self.ask_for_fixed(out_inv + err_inv))
        return None

    def prepare_file(self, file: Path, prg: str):
        self.text_description = None
        if self.config.include_text_descriptions:
            text_description_file = file.parent / "text-descriptions" / f"{file.stem}.txt"
            self.text_description = text_description_file.read_text()
            self.logger.info(f"Text description: {self.text_description}")

        self.starting_prg = prg
        self.name = file.name

    def run_on_file(
        self,
        mode: Mode,
        total_tries: int,
        file: str,
    ) -> Optional[int]:
        self.logger.info(f"Running on {file}")

        file_path = Path(file)
        with file_path.open() as f:
            prg = f.read()
        self.prepare_file(file_path, prg)
        prg = self.preprocess(prg, mode)
        assert self.name is not None
        verification_result = self.verify_program(self.name, 0, self.postprocess(prg))
        if verification_result is not None and verification_result[0]:
            return 0
        elif verification_result is None:
            self.logger.info(f"Verification timed out for {self.name}")
        if total_tries == 0:
            return None
        self.precheck(prg, mode)
        inv_prg = self.postprocess(self.invoke(prg, mode, self.text_description))
        return self.try_fixing(total_tries, inv_prg, self.name)
