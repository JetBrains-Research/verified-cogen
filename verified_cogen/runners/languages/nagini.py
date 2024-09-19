import re
from typing import Pattern

from verified_cogen.runners.languages.language import GenericLanguage

NAGINI_VALIDATOR_TEMPLATE = """\
def {method_name}_valid({parameters}) -> {returns}:{specs}\
    ret = {method_name}({param_names})
    return ret\
"""


class NaginiLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self):
        super().__init__(
            re.compile(
                r"def\s+(\w+)\s*\((.*?)\)\s*->\s*(.*?):(.*?(\r\n|\r|\n))\s+# impl-start",
                re.DOTALL,
            ),
            NAGINI_VALIDATOR_TEMPLATE,
            [
                r" *# assert-start.*?# assert-end\n?",
                r" *# invariants-start.*?# invariants-end\n?",
            ],
            "# assert-line",
            "#",
        )
