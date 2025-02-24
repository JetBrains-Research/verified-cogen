from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from verified_cogen.llm.llm import LLM


@dataclass
class LLMConfig:
    temperature: float
    grazie_token: str
    llm_profile: str
    prompts_directory: list[str]

    def build(self, idx: int, history: Optional[Path] = None) -> LLM:
        return LLM(
            self.grazie_token,
            self.llm_profile,
            self.prompts_directory[idx],
            self.temperature,
            history=history,
        )


@dataclass
class IOConfig:
    max_jobs: int
    skip_failed: bool


@dataclass
class ProgramConfig:
    directory: Path
    tries: int
    runs: int
    insert_conditions_mode: str
    bench_types: list[str]
    manual_rewriters: list[str]
    log_tries_directory: Optional[Path]
    results_directory: Path

    llm: LLMConfig
    io: IOConfig
