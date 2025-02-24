from typing import Optional

from verified_cogen.runners.rewriters import Rewriter


class NaginiRewriter(Rewriter):
    def rewrite(self, prg: str, error: Optional[str] = None) -> tuple[str, str]:
        pos_implications: list[tuple[int, int]] = []

        for idx, line in enumerate(prg.splitlines()):
            for j in range(0, len(line) - 2):
                if line[j : j + 3] == "==>":
                    pos_implications.append((idx + 1, j + 1))

        if len(pos_implications) == 0:
            return prg, ""

        prompt = (
            "Manual inspection revealed occurrences of `==>` operator for implication on the following positions:\n"
        )
        prompt += ", ".join(f"({a}, {b})" for a, b in pos_implications) + "\n"
        prompt += "`==>` operator does not exist in Nagini. All occurrences of `==>` operator should be replaced with `Implies(a, b)` operator, that is used to express implication in Nagini\n"

        return prg, prompt
