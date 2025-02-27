from typing import Optional

from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.runners.rewriters.nagini_rewriter import NaginiRewriter
from verified_cogen.runners.rewriters.nagini_rewriter_fixing import NaginiRewriterFixing
from verified_cogen.runners.rewriters.nagini_rewriter_fixing_ast import NaginiRewriterFixingAST


def construct_nagini_rewriter(runner_types: list[str]) -> Optional[Rewriter]:
    runner = None
    for runner_type in runner_types:
        if runner_type == "NaginiRewriter":
            runner = NaginiRewriter()
        elif runner_type == "NaginiRewriterFixing":
            runner = NaginiRewriterFixing(runner)
        elif runner_type == "NaginiRewriterFixingAST":
            runner = NaginiRewriterFixingAST(runner)
        else:
            raise ValueError(f"Unexpected nagini rewriter type: {runner_type}")
    return runner


def construct_rewriter(extension: str, runner_types: list[str]) -> Optional[Rewriter]:
    if extension == "py":
        return construct_nagini_rewriter(runner_types)
    if runner_types:
        raise ValueError(f"Not implemented rewriters for language: {LanguageDatabase().regularise[extension]}")
    return None
