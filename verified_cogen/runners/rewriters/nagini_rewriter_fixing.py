from typing import Optional

from verified_cogen.runners.rewriters.__init__ import Rewriter


class NaginiRewriterFixing(Rewriter):
    wrapped_rewriter: Optional[Rewriter]

    def __init__(self, rewriter: Optional[Rewriter] = None):
        super().__init__()
        self.wrapped_rewriter = rewriter

    def replace_impl(self, prg: str):
        indices: list[tuple[int, str]] = []

        for i in range(len(prg) - 2):
            if prg[i : i + 3] == "==>":
                cnt = 0
                for j in range(i - 1, -1, -1):
                    if cnt == 0 and (prg[j] == ":" or prg[j] == "(" or j >= 2 and prg[j - 2 : j + 1] == "==>"):
                        indices.append((j, "Implies("))
                        break
                    if prg[j] == "(":
                        cnt -= 1
                    elif prg[j] == ")":
                        cnt += 1
                cnt = 0
                for j in range(i + 3, len(prg)):
                    if cnt == 0 and prg[j] == ")":
                        indices.append((j - 1, ")"))
                        break
                    if prg[j] == ")":
                        cnt -= 1
                    elif prg[j] == "(":
                        cnt += 1

        dict_: dict[int, str] = {}
        for i, st in indices:
            if i not in dict_:
                dict_[i] = ""
            dict_[i] = dict_[i] + st

        new_prg = ""

        j = 0
        while j < len(prg):
            if j < len(prg) - 2 and prg[j : j + 3] == "==>":
                j = j + 2
                new_prg += ","
            else:
                new_prg += prg[j]
            if j in dict_:
                for s in dict_[j]:
                    new_prg += s
            j = j + 1

        return new_prg

    def rewrite(self, prg: str, error: Optional[str] = None) -> tuple[str, str]:
        prompt: str = ""

        if self.wrapped_rewriter is not None:
            prg, prompt = self.wrapped_rewriter.rewrite(prg)

        if prompt == "":
            return prg, ""

        prompt += "We fixed errors with `==>` occurrences for you, and got the following program:\n"

        new_prg = self.replace_impl(prg)

        prompt += new_prg + "\n"

        prompt += "Next, we run verifier on this program. Using the following verdict, you should possibly modify this program.\n"

        return new_prg, prompt
