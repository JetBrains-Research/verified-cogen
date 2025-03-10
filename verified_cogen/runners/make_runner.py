from logging import Logger
from typing import Callable, Optional

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner, RunnerConfig
from verified_cogen.runners.flush import FlushRunner
from verified_cogen.runners.generate import GenerateRunner
from verified_cogen.runners.generic import GenericRunner
from verified_cogen.runners.invariants import InvariantRunner
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.runners.step_by_step import StepByStepRunner
from verified_cogen.runners.testing import TestingRunner
from verified_cogen.runners.validating import ValidatingRunner
from verified_cogen.tools.verifier import Verifier


def make_runner_cls(
    bench_type: str, extension: str, config: RunnerConfig
) -> Callable[[LLM, Logger, Verifier, Optional[Rewriter]], Runner]:
    def runner_cls(
        llm: LLM,
        logger: Logger,
        verifier: Verifier,
        rewriter: Optional[Rewriter] = None,
    ):
        if bench_type == "invariants":
            return InvariantRunner(llm, logger, verifier, config)
        elif bench_type == "generic":
            return GenericRunner(llm, logger, verifier, config)
        elif bench_type == "generate":
            return GenerateRunner(llm, logger, verifier, config)
        elif bench_type == "validating":
            return ValidatingRunner(
                InvariantRunner(llm, logger, verifier, config, rewriter),
                LanguageDatabase().get(extension),
            )
        elif bench_type == "testing":
            return ValidatingRunner(
                TestingRunner(
                    InvariantRunner(llm, logger, verifier, config, rewriter),
                    LanguageDatabase().get(extension)
                ),
                LanguageDatabase().get(extension)
            )
        elif bench_type == "step-by-step":
            return ValidatingRunner(
                StepByStepRunner(InvariantRunner(llm, logger, verifier, config, rewriter)),
                LanguageDatabase().get(extension),
            )
        elif bench_type == "step-by-step-flush":
            return ValidatingRunner(
                FlushRunner(StepByStepRunner(InvariantRunner(llm, logger, verifier, config, rewriter))),
                LanguageDatabase().get(extension),
            )
        else:
            raise ValueError(f"Unexpected bench_type: {bench_type}")

    return runner_cls
