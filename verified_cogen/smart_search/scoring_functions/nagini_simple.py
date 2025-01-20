from typing import List, Tuple
import re

from verified_cogen.smart_search.scoring_functions import ScoringFunction


class NaginiSimpleScoringFunction(ScoringFunction):
    error_penalty: float
    long_penalty: float
    standard_errors: List[str] = [
        "The precondition of",
        "Postcondition of",
        "Loop invariant might not be preserved",
        "Loop invariant might not hold on entry",
        "Assert might fail",
    ]

    def __init__(self, error_penalty: float, long_penalty: float):
        self.error_penalty = error_penalty
        self.long_penalty = long_penalty

    def count_functions(self, prg: str, message: str) -> Tuple[int, int]:
        pattern = r"@(\d+)\."
        error_lines = [int(num) - 1 for num in re.findall(pattern, message)]
        lines_with_defs = [
            i for i, line in enumerate(prg.splitlines()) if "def" in line
        ]

        ver, unver = 0, 0
        for i in range(len(lines_with_defs)):
            if (
                i == len(lines_with_defs) - 1
                and all(
                    line < lines_with_defs[i] or line >= len(prg)
                    for line in error_lines
                )
                or i < len(lines_with_defs) - 1
                and all(
                    line < lines_with_defs[i] or line >= lines_with_defs[i + 1]
                    for line in error_lines
                )
            ):
                ver += 1
            else:
                unver += 1

        return ver, unver

    def score(self, prg: str, message: str) -> float:
        if message == "Verification timed out" or len(message.splitlines()) > 20:
            return self.long_penalty

        if "Translation failed" in message:
            return -1e9

        error_count = sum(message.count(err) for err in self.standard_errors)

        ver, unver = self.count_functions(prg, message)

        return (ver - self.error_penalty * error_count) / (ver + unver)
