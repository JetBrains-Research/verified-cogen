import re
from re import Pattern

from verified_cogen.runners.languages.language import AnnotationType, GenericLanguage

DAFNY_VALIDATOR_TEMPLATE = """\
method {method_name}_valid({parameters}) returns ({returns}){specs}\
{ var {return_values} := {method_name}({param_names}); return {return_values}; }
"""

DAFNY_VALIDATOR_TEMPLATE_VOID = """\
method {method_name}_valid({parameters}){specs}\
{ {method_name}({param_names}); }
"""

DAFNY_VALIDATOR_TEMPLATE_PURE_COPY = """\
function {method_name}_copy_pure({parameters}):{returns} {specs}\
{ 
    {body} 
}
"""

DAFNY_VALIDATOR_TEMPLATE_PURE = """\
function {method_name}_valid_pure({parameters}):{returns} {specs}\
{ {method_name}({param_names}) }
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
            AnnotationType.PURE: r"(function|lemma|predicate|class).*?// pure-end\n",
        }
        super().__init__(
            re.compile(r"method\s+(\w+)\s*\((.*?)\)\s*returns\s*\((.*?)\)(.*?)\{", re.DOTALL),
            re.compile(
                r"function\s+(\w+)\s*\((.*?)\) *: *(.*?)\s*(.*?)\{(.*?)}",
                re.DOTALL,
            ),
            re.compile(r"method\s+(\w+)\s*\((.*?)\)(.*?)\{", re.DOTALL),
            DAFNY_VALIDATOR_TEMPLATE,
            DAFNY_VALIDATOR_TEMPLATE_PURE,
            DAFNY_VALIDATOR_TEMPLATE_PURE_COPY,
            DAFNY_VALIDATOR_TEMPLATE_VOID,
            AnnotationType.PURE in remove_annotations,
            [annotation_by_type[annotation_type]for annotation_type in remove_annotations],
            "// assert-line" if AnnotationType.ASSERTS in remove_annotations else None,
            "//",
        )

    def _validators_from(self, method_name: str, parameters: str, returns: str, specs: str) -> str:
        result = super()._validators_from(method_name, parameters, returns, specs)
        result = result.replace(
            "{return_values}",
            ", ".join(f"ret{i}" for i in range(len(returns.split(",")))),
        )
        return result

    def separate_validator_errors(self, errors: str) -> tuple[str, str]:
        lines = errors.split("\n")
        lines = [line for line in lines if "Dafny program verifier finished" not in line]
        line_with_ret0 = next((i for i, line in enumerate(lines) if "ret0" in line), None)
        if line_with_ret0 is None:
            return "\n".join(lines), ""
        else:
            non_verifier_errors = "\n".join(lines[: line_with_ret0 - 2]).strip()
            verifier_errors = "\n".join(lines[line_with_ret0 - 2 :]).strip()
            return non_verifier_errors, verifier_errors
