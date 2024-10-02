import re
from typing import Pattern

from verified_cogen.runners.languages.language import GenericLanguage

DAFNY_VALIDATOR_TEMPLATE = """\
method {method_name}_valid({parameters}) returns ({returns}){specs}\
{ var {return_values} := {method_name}({param_names}); return {return_values}; }
"""


class DafnyLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self):  # type: ignore
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
            "//",
        )

    def _validators_from(
        self, method_name: str, parameters: str, returns: str, specs: str
    ) -> str:
        result = super()._validators_from(method_name, parameters, returns, specs)
        result = result.replace(
            "{return_values}",
            ", ".join(f"ret{i}" for i in range(len(returns.split(",")))),
        )
        return result
