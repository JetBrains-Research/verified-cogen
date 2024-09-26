import re
from typing import Pattern

from verified_cogen.runners.languages.language import GenericLanguage

VERUS_VALIDATOR_TEMPLATE = """\
fn {method_name}_valid({parameters}) -> ({returns}){specs}\
{ let ret = {method_name}({param_names}); ret }
"""


class VerusLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self):  # type: ignore
        super().__init__(
            re.compile(
                r"^\s*fn\s+(\w+)\s*\((.*?)\)\s*->\s*\((.*?)\)(.*?)\{",
                flags=re.DOTALL | re.MULTILINE,
            ),
            VERUS_VALIDATOR_TEMPLATE,
            [
                r" *// assert-start.*?// assert-end\n",
                r" *// invariants-start.*?// invariants-end\n",
            ],
            "// assert-line",
            "//",
        )

    def generate_validators(self, code: str) -> str:
        result = super().generate_validators(code)
        return "verus!{{\n{}}}".format(result)
