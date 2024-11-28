from abc import abstractmethod
from enum import Enum
from typing import Any, Pattern, List, Tuple


class AnnotationType(Enum):
    INVARIANTS = "invariants"
    ASSERTS = "asserts"
    PRE_CONDITIONS = "pre-conditions"
    POST_CONDITIONS = "post-conditions"
    IMPLS = "impls"


class Language:
    simple_comment: str

    @abstractmethod
    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]): ...

    @abstractmethod
    def generate_validators(self, code: str) -> str: ...

    @abstractmethod
    def remove_conditions(self, code: str) -> str: ...

    @abstractmethod
    def separate_validator_errors(self, errors: str) -> tuple[str, str]: ...

    @abstractmethod
    def check_helpers(
        self, code: str, pure_non_helpers: [str]
    ) -> Tuple[List[str], str]: ...

    @abstractmethod
    def find_pure_non_helpers(self, code: str) -> [str]: ...


class GenericLanguage(Language):
    method_regex: Pattern[str]
    validator_template: str
    check_patterns: list[str]
    inline_assert_comment: str

    def __init__(  # type: ignore
        self,
        method_regex: Pattern[str],
        validator_template: str,
        check_patterns: list[str],
        inline_assert_comment: str,
        simple_comment: str,
    ):
        self.simple_comment = simple_comment
        self.method_regex = method_regex
        self.validator_template = validator_template
        self.check_patterns = check_patterns
        self.inline_assert_comment = inline_assert_comment

    def _validators_from(
        self,
        method_name: str,
        parameters: str,
        returns: str,
        specs: str,
    ) -> str:
        return (
            self.validator_template.replace("{method_name}", method_name)
            .replace("{parameters}", parameters or "")
            .replace("{returns}", returns or "")
            .replace("{specs}", specs or "\n")
            .replace(
                "{param_names}",
                ", ".join(
                    param.split(":")[0].strip()
                    for param in parameters.split(",")
                    if param.strip()
                ),
            )
        )

    def generate_validators(self, code: str) -> str:
        methods = list(self.method_regex.finditer(code))

        validators: list[str] = []

        for match in methods:
            method_name, parameters, returns, specs = (
                match.group(1),
                match.group(2),
                match.group(3),
                match.group(4),
            )

            validators.append(
                self._validators_from(method_name, parameters, returns, specs)
            )

        return "\n".join(validators)

    def remove_conditions(self, code: str) -> str:
        import re

        cleaned_code = code
        for pattern in self.check_patterns:
            cleaned_code = re.sub(pattern, "", cleaned_code, flags=re.DOTALL)
        cleaned_code = re.sub(r"\n\s*\n", "\n", cleaned_code)
        lines = cleaned_code.split("\n")
        lines = [line for line in lines if self.inline_assert_comment not in line]
        return "\n".join(lines).strip()

    def check_helpers(
        self, code: str, pure_non_helpers: [str]
    ) -> Tuple[List[str], str]:
        return [], code

    def find_pure_non_helpers(self, code: str) -> [str]:
        return []


class LanguageDatabase:
    _instance = None
    languages: dict[str, Language] = dict()
    regularise: dict[str, str] = dict()

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def register(self, name: str, aliases: list[str], definition: Language):
        self.languages[name] = definition
        self.regularise[name] = name
        for alias in aliases:
            self.regularise[alias] = name

    def get(self, name: str):
        if name not in self.regularise:
            raise ValueError(f"language {name} not found, has it been registered?")
        return self.languages[self.regularise[name]]
