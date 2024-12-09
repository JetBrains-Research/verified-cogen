import re
from typing import Pattern

from verified_cogen.runners.languages.language import AnnotationType, GenericLanguage

VERUS_VALIDATOR_TEMPLATE = """\
fn {method_name}_valid({parameters}) -> ({returns}){specs}\
{ let ret = {method_name}({param_names}); ret }
"""

VERUS_VALIDATOR_TEMPLATE_PURE = """\
spec fn {method_name}_valid({parameters}) -> ({returns}){specs}\
{ 
    {body}
}
"""


class VerusLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self, remove_annotations: list[AnnotationType]):  # type: ignore
        annotation_by_type = {
            AnnotationType.INVARIANTS: r" *// invariants-start.*?// invariants-end\n",
            AnnotationType.ASSERTS: r" *// assert-start.*?// assert-end\n",
            AnnotationType.PRE_CONDITIONS: r" *// pre-conditions-start.*?// pre-conditions-end\n",
            AnnotationType.POST_CONDITIONS: r" *// post-conditions-start.*?// post-conditions-end\n",
            AnnotationType.IMPLS: r" *// impl-start.*?// impl-end\n",
            AnnotationType.PURE: r"spec fn.*?// pure-end\n",
        }
        super().__init__(
            re.compile(
                r"^\s*fn\s+(\w+)\s*\((.*?)\)\s*->\s*\((.*?)\)(.*?)\{",
                flags=re.DOTALL | re.MULTILINE,
            ),
            re.compile(
                r"^\s*spec fn\s+(\w+)\s*\((.*?)\)\s*->\s*\((.*?)\)(.*?)\{",
                flags=re.DOTALL | re.MULTILINE,
            ),
            VERUS_VALIDATOR_TEMPLATE,
            VERUS_VALIDATOR_TEMPLATE_PURE,
            [
                annotation_by_type[annotation_type]
                for annotation_type in remove_annotations
            ],
            "// assert-line",
            "//",
        )

    def generate_validators(self, code: str) -> str:
        result = super().generate_validators(code)
        return "verus!{{\n{}}}".format(result)

    def separate_validator_errors(self, errors: str) -> tuple[str, str]:
        raise NotImplementedError(
            "Separating validator errors is not implemented for Verus yet"
        )
