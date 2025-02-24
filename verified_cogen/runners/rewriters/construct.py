from typing import Optional

from verified_cogen.config import LLMConfig
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.runners.rewriters.nagini_rewriter import NaginiRewriter
from verified_cogen.runners.rewriters.nagini_rewriter_fixing import NaginiRewriterFixing
from verified_cogen.runners.rewriters.nagini_rewriter_fixing_ast import NaginiRewriterFixingAST
from verified_cogen.runners.rewriters.verus_rewriter import VerusRewriter


def construct_nagini_rewriter(runner_types: list[str]) -> Optional[Rewriter]:
    runner = None
    for runner_type in runner_types:
        match runner_type:
            case "NaginiRewriter":
                runner = NaginiRewriter()
            case "NaginiRewriterFixing":
                runner = NaginiRewriterFixing(runner)
            case "NaginiRewriterFixingAST":
                runner = NaginiRewriterFixingAST(runner)
            case _:
                raise ValueError(f"Unexpected nagini rewriter type: {runner_type}")
    return runner


def construct_verus_rewriter(runner_types: list[str], llm: tuple[LLMConfig, int]) -> Optional[Rewriter]:
    runner = None
    for runner_type in runner_types:
        match runner_type:
            case "VerusRewriter":
                runner = VerusRewriter(llm)
            case _:
                raise ValueError(f"Unexpected verus rewriter type: {runner_type}")
    return runner


def construct_rewriter(extension: str, llm: tuple[LLMConfig, int], runner_types: list[str]) -> Optional[Rewriter]:
    match extension:
        case "py":
            return construct_nagini_rewriter(runner_types)
        case "rs":
            return construct_verus_rewriter(runner_types, llm)
        case _ if runner_types:
            raise ValueError(f"Not implemented rewriters for language: {LanguageDatabase().regularise[extension]}")
        case _:
            return None
