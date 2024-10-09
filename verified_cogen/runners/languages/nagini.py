import re
from typing import Pattern

from verified_cogen.runners.languages.language import AnnotationType, GenericLanguage

NAGINI_VALIDATOR_TEMPLATE = """\
def {method_name}_valid({parameters}) -> {returns}:{specs}\
    ret = {method_name}({param_names})
    return ret\
"""


class NaginiLanguage(GenericLanguage):
    method_regex: Pattern[str]

    def __init__(self, remove_annotations: list[AnnotationType]):  # type: ignore
        annotation_by_type = {
            AnnotationType.INVARIANTS: r" *# invariants-start.*?# invariants-end\n?",
            AnnotationType.ASSERTS: r" *# assert-start.*?# assert-end\n?",
            AnnotationType.PRE_CONDITIONS: r" *# pre-conditions-start.*?# pre-conditions-end\n?",
            AnnotationType.POST_CONDITIONS: r" *# post-conditions-start.*?# post-conditions-end\n?",
        }
        super().__init__(
            re.compile(
                r"def\s+(\w+)\s*\((.*?)\)\s*->\s*(.*?):(.*?(\r\n|\r|\n))\s+# impl-start",
                re.DOTALL,
            ),
            NAGINI_VALIDATOR_TEMPLATE,
            [
                annotation_by_type[annotation_type]
                for annotation_type in remove_annotations
            ],
            "# assert-line",
            "#",
        )
