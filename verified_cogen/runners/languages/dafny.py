import re
from typing import Pattern

from verified_cogen.runners.languages.language import AnnotationType, GenericLanguage

DAFNY_VALIDATOR_TEMPLATE = """\
method {method_name}_valid({parameters}) returns ({returns}){specs}\
{ {return_values} := {method_name}({param_names}); }
"""


class DafnyLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self, remove_annotations: list[AnnotationType]):  # type: ignore
        annotation_by_type = {
            AnnotationType.INVARIANTS: r" *// invariants-start.*?// invariants-end\n",
            AnnotationType.ASSERTS: r" *// assert-start.*?// assert-end\n",
            AnnotationType.PRE_CONDITIONS: r" *// pre-conditions-start.*?// pre-conditions-end\n",
            AnnotationType.POST_CONDITIONS: r" *// post-conditions-start.*?// post-conditions-end\n",
            AnnotationType.IMPLS: r" *// impl-start.*?// impl-end\n",
        }
        super().__init__(
            re.compile(
                r"method\s+(\w+)\s*\((.*?)\)\s*returns\s*\((.*?)\)(.*?)\{", re.DOTALL
            ),
            DAFNY_VALIDATOR_TEMPLATE,
            [
                annotation_by_type[annotation_type]
                for annotation_type in remove_annotations
            ],
            "// assert-line",
            "//",
        )

    def _validators_from(
        self, method_name: str, parameters: str, returns: str, specs: str
    ) -> str:
        # Rename return values to neutral names to avoid collisions in cases like 037-sort_even
        # method sorted_even(a: seq<int>) returns (sorted_even: seq<int>)
        #                                          ^^^ - is a variable
        # method sorted_even_valid(a: seq<int>) returns (sorted_even: seq<int>)
        #                                                ^^^ - is the above function, invalid name
        renamed_returns = [(f"ret{i}", r.split(":")) for i, r in enumerate(returns.split(","))]
        modified_specs = specs
        for n, (r, t) in renamed_returns:
            modified_specs = modified_specs.replace(r, n)
        result = super()._validators_from(
            method_name,
            parameters,
            ", ".join(f"{n}:{t[1]}" for n, t in renamed_returns),
            modified_specs
        )
        result = result.replace(
            "{return_values}",
            ", ".join(n for n, _ in renamed_returns),
        )
        return result

    def separate_validator_errors(self, errors: str) -> tuple[str, str]:
        lines = errors.split("\n")
        lines = [
            line for line in lines if "Dafny program verifier finished" not in line
        ]
        line_with_ret0 = next(
            (i for i, line in enumerate(lines) if "ret0" in line), None
        )
        if line_with_ret0 is None:
            return "\n".join(lines), ""
        else:
            non_verifier_errors = "\n".join(lines[: line_with_ret0 - 2]).strip()
            verifier_errors = "\n".join(lines[line_with_ret0 - 2 :]).strip()
            return non_verifier_errors, verifier_errors
