import re
from typing import Pattern

from verified_cogen.runners.languages.language import GenericLanguage

DAFNY_VALIDATOR_TEMPLATE = """\
method {method_name}_valid({parameters}) returns ({returns}){specs}\
{ var ret := {method_name}({param_names}); return ret; }
"""


class DafnyLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self):
        super().__init__(
            re.compile(
                r"method\s+(\w+)\s*\((.*?)\)\s*returns\s*\((.*?)\)(.*?)\{", re.DOTALL
            ),
            DAFNY_VALIDATOR_TEMPLATE,
            [
                r" *// assert-start.*?// assert-end\n",
                r" *// invariants-start.*?// invariants-end\n",
            ],
            "// assert-line",
        )
