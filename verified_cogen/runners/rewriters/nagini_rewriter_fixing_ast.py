from typing import Optional, Tuple

from verified_cogen.runners.rewriters.__init__ import Rewriter
from verified_cogen.tools.inequality_replacer import (
    contains_double_inequality,
    replace_inequalities,
)


class NaginiRewriterFixingAST(Rewriter):
    wrapped_rewriter: Optional[Rewriter]

    def __init__(self, rewriter: Optional[Rewriter] = None):
        super().__init__()
        self.wrapped_rewriter = rewriter

    def rewrite(self, prg: str) -> Tuple[str, str]:
        prompt: str = ""

        if self.wrapped_rewriter is not None:
            prg, prompt = self.wrapped_rewriter.rewrite(prg)

        try:
            if contains_double_inequality(prg):
                prg = replace_inequalities(prg)
                prompt += "We replaced all double (triple and so on) inequalities with their equivalents (as they are prohibited) and got the following program:\n"
                prompt += prg + "\n"
                prompt += "Next, we run verifier on this program. Using the following verdict, you should possibly modify this program.\n"
        except Exception:
            pass

        return prg, prompt
