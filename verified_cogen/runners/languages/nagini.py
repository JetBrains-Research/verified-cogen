from typing import Pattern
from verified_cogen.runners.languages.language import GenericLanguage
import re

NAGINI_VALIDATOR_TEMPLATE = """\
def {method_name}_valid({parameters}) -> {returns}:{specs}
    ret = {method_name}({param_names})
    return ret
"""


class NaginiLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self):
        super().__init__(
            re.compile(r"def\s+(\w+)\s*\((.*?)\)\s*->\s*(.*?):(.*?)", re.DOTALL),
            NAGINI_VALIDATOR_TEMPLATE,
        )
