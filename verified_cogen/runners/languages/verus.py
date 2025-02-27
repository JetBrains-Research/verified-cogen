import re
from re import Pattern

from verified_cogen.runners.languages.language import AnnotationType, GenericLanguage

VERUS_VALIDATOR_TEMPLATE = """\
fn {method_name}_valid({parameters}) -> ({returns}){specs}\
{ let ret = {method_name}({param_names}); ret }
"""

VERUS_VALIDATOR_TEMPLATE_VOID = """\
fn {method_name}_valid({parameters}){specs}\
{ {method_name}({param_names}); }
"""

VERUS_VALIDATOR_TEMPLATE_PURE_COPY = """\
spec fn {method_name}_copy_pure({parameters}) -> ({returns}){specs}\
{{body}}
"""

VERUS_VALIDATOR_TEMPLATE_PURE = """\
spec fn {method_name}_valid_pure({parameters}) -> ({returns}){specs}\
{ let ret = {method_name}({param_names}); ret }
"""


class VerusLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self, remove_annotations: list[AnnotationType]):  # type: ignore
        annotation_by_type = {
            AnnotationType.INVARIANTS: r" *// invariants-start.*?// invariants-end\n?",
            AnnotationType.ASSERTS: r" *// assert-start.*?// assert-end\n?",
            AnnotationType.PRE_CONDITIONS: r" *// pre-conditions-start.*?// pre-conditions-end\n?",
            AnnotationType.POST_CONDITIONS: r" *// post-conditions-start.*?// post-conditions-end\n?",
            AnnotationType.IMPLS: r" *// impl-start.*?// impl-end\n?",
            AnnotationType.PURE: r" *(spec fn|proof fn).*?// pure-end\n?",
        }
        super().__init__(
            re.compile(
                r"^fn\s+(\w+)\s*\((.*?)\)\s*->\s*\((.*?)\)(.*?)\{",
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                r"^spec fn\s+(\w+)\s*\((.*?)\)\s*-> *\((.*?)\)(.*?)\{(.*?)}\n// pure-end",
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                r"^fn\s+(\w+)\s*\((.*?)\)(.*?)\{",
                flags=re.DOTALL | re.MULTILINE,
            ),
            VERUS_VALIDATOR_TEMPLATE,
            VERUS_VALIDATOR_TEMPLATE_PURE,
            VERUS_VALIDATOR_TEMPLATE_PURE_COPY,
            VERUS_VALIDATOR_TEMPLATE_VOID,
            AnnotationType.PURE in remove_annotations,
            [annotation_by_type[annotation_type] for annotation_type in remove_annotations],
            "// assert-line",
            "//",
        )

    def split_params(self, parameters: str) -> str:
        pattern = r"(\w+)\s*:\s*((?:\[[^\[\]]*\]|\([^()]*\)|[^\[\],])+)"
        matches = re.findall(pattern, parameters)
        return ", ".join([var.strip() for var, _ in matches])

    def generate_validators(self, code: str, validate_helpers: bool) -> str:
        result = super().generate_validators(code, validate_helpers)
        return f"verus!{{\n{result}}}"

    def separate_validator_errors(self, errors: str) -> tuple[str, str]:
        lines = errors.split("\n")
        lines = [line for line in lines if "verification results" not in line]
        return "\n".join(lines), ""
