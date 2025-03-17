from pathlib import Path
from typing import Optional

from verified_cogen.runners import Runner
from verified_cogen.runners.languages.language import Language
from verified_cogen.tools.modes import Mode


class TestingRunner(Runner):
    wrapped_runner: Runner
    language: Language

    def __init__(self, wrapping: Runner, language: Language):
        super().__init__(wrapping.llm, wrapping.logger, wrapping.verifier, wrapping.config)
        self.wrapped_runner = wrapping
        self.language = language

    def _add_tests(self, inv_prg: str) -> str:
        if self.tests is None:
            return inv_prg
        test_prg = inv_prg + "\n" + self.language.simple_comment + " ==== tests ==== \n" + self.tests
        return test_prg

    def preprocess(self, prg: str, mode: Mode) -> str:
        self.wrapped_runner.starting_prg = prg
        return prg

    def verify_program(self, name: str, try_n: int, prg: str, tag: str = "") -> Optional[tuple[bool, str, str]]:
        full_name = Runner.combine_name(name, try_n, tag)
        base_verif = self.wrapped_runner.verify_program(name, try_n, prg, tag)
        if base_verif is None or not base_verif[0] or self.tests is None:
            return base_verif

        tests_prg = self._add_tests(prg)
        working_dir = self._base_dir() / full_name.rsplit(".", 1)[0]
        working_dir.mkdir(parents=True, exist_ok=True)
        output = working_dir / full_name
        with open(output, "w") as f:
            f.write(tests_prg)
        tests_verif = self.verifier.test(output)
        if self.config.record_history and tests_verif is not None:
            self._history[full_name] = tests_verif
        return tests_verif

    @property
    def history(self):
        return self._history | self.wrapped_runner.history

    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
        return self.wrapped_runner.rewrite(prg, text_description, additional_prompt)

    def produce(self, prg: str) -> str:
        return self.wrapped_runner.produce(prg)

    def insert(self, prg: str, checks: str, mode: Mode) -> str:
        return self.wrapped_runner.insert(prg, checks, mode)

    def ask_for_timeout(self) -> str:
        assert self.starting_prg is not None
        return self.wrapped_runner.ask_for_timeout()

    def ask_for_fixed(self, err: str) -> str:
        assert self.starting_prg is not None
        return self.wrapped_runner.ask_for_fixed(err)

    def precheck(self, prg: str, mode: Mode):
        return self.wrapped_runner.precheck(prg, mode)

    def prepare_file(self, file: Path, prg: str):
        super().prepare_file(file, prg)
        self.wrapped_runner.prepare_file(file, prg)
        self.tests = None
        test_file = file.parent / "tests" / file.name
        if test_file.exists():
            self.tests = test_file.read_text()
