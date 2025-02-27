import re
from re import Pattern

from verified_cogen.runners.languages.language import AnnotationType, GenericLanguage
from verified_cogen.tools.pureCallsDetectors import detect_and_replace_pure_calls_nagini

NAGINI_VALIDATOR_TEMPLATE = """\

def {method_name}_valid({parameters}) -> {returns}:{specs}\
\n
    ret = {method_name}({param_names})
    return ret\
"""

NAGINI_VALIDATOR_TEMPLATE_VOID = """\

def {method_name}_valid({parameters}):{specs}\
\n
    {method_name}({param_names})\
"""

NAGINI_VALIDATOR_TEMPLATE_PURE_COPY = """
@Pure
def {method_name}_copy_pure({parameters}) -> {returns}:{specs}\
{body}"""

NAGINI_VALIDATOR_TEMPLATE_PURE = """
@Pure
def {method_name}_valid_pure({parameters}) -> {returns}:{specs}\
\n
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
            AnnotationType.IMPLS: r" *# impl-start.*?# impl-end\n",
            AnnotationType.PURE: r"@Pure\ndef.*?# pure-end\n",
        }
        super().__init__(
            re.compile(
                r"def\s+(\w+)\s*\((.*?)\)\s*->\s*(.*?):(.*?)\s+# (impl-start|pure-start)",
                re.DOTALL,
            ),
            re.compile(
                r"@Pure\s+def\s+(\w+)\s*\((.*?)\)\s*->\s*(.*?):(.*?)\s+# pure-start(.*?)\s+# pure-end",
                re.DOTALL,
            ),
            re.compile(
                r"def\s+(\w+)\s*\((.*?)\)\s*:(.*?)\s+# (impl-start|pure-start)",
                re.DOTALL,
            ),
            NAGINI_VALIDATOR_TEMPLATE,
            NAGINI_VALIDATOR_TEMPLATE_PURE,
            NAGINI_VALIDATOR_TEMPLATE_PURE_COPY,
            NAGINI_VALIDATOR_TEMPLATE_PURE_COPY,
            AnnotationType.PURE in remove_annotations,
            [annotation_by_type[annotation_type] for annotation_type in remove_annotations],
            "# assert-line",
            "#",
        )

    def separate_validator_errors(self, errors: str) -> tuple[str, str]:
        lines = errors.split("\n")
        lines = [line for line in lines if "Verification successful" not in line and "Verification took" not in line]
        return "\n".join(lines), ""

    def check_helpers(self, code: str, pure_non_helpers: list[str]) -> tuple[list[str], str]:
        return detect_and_replace_pure_calls_nagini(code, pure_non_helpers)

    def find_pure_non_helpers(self, code: str) -> list[str]:
        pattern: Pattern[str] = re.compile(
            r"#use-as-unpure\s+@Pure\s+def\s+(\w+)\s*\((.*?)\)\s*->\s*(.*?):",
            re.DOTALL,
        )
        methods = list(pattern.finditer(code))
        non_helpers: list[str] = []
        for match in methods:
            non_helpers.append(match.group(1))
        return non_helpers
