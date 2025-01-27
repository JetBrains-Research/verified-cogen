from abc import abstractmethod
from enum import Enum
from typing import Any, List, Pattern, Tuple


class AnnotationType(Enum):
    INVARIANTS = "invariants"
    ASSERTS = "asserts"
    PRE_CONDITIONS = "pre-conditions"
    POST_CONDITIONS = "post-conditions"
    IMPLS = "impls"
    PURE = "pure"


class Language:
    simple_comment: str

    @abstractmethod
    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]): ...

    @abstractmethod
    def generate_validators(self, code: str, validate_helpers: bool) -> str: ...

    @abstractmethod
    def remove_conditions(self, code: str) -> str: ...

    @abstractmethod
    def separate_validator_errors(self, errors: str) -> tuple[str, str]: ...

    @abstractmethod
    def check_helpers(
        self, code: str, pure_non_helpers: List[str]
    ) -> Tuple[List[str], str]: ...

    @abstractmethod
    def find_pure_non_helpers(self, code: str) -> List[str]: ...


class GenericLanguage(Language):
    method_regex: Pattern[str]
    pure_regex: Pattern[str]
    validator_template: str
    check_patterns: list[str]
    inline_assert_comment: str
    remove_pure: bool

    def __init__(  # type: ignore
        self,
        method_regex: Pattern[str],
        pure_regex: Pattern[str],
        validator_template: str,
        validator_template_pure: str,
        validator_template_pure_copy: str,
        remove_pure: bool,
        check_patterns: list[str],
        inline_assert_comment: str,
        simple_comment: str,
    ):
        self.simple_comment = simple_comment
        self.method_regex = method_regex
        self.pure_regex = pure_regex
        self.validator_template = validator_template
        self.validator_template_pure = validator_template_pure
        self.validator_template_pure_copy = validator_template_pure_copy
        self.check_patterns = check_patterns
        self.inline_assert_comment = inline_assert_comment
        self.remove_pure = remove_pure

    def split_params(self, parameters: str) -> str:
        return ", ".join(
            param.split(":")[0].strip()
            for param in parameters.split(",")
            if param.strip()
        )

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
                self.split_params(parameters),
            )
        )

    def _validators_from_pure_copy(
        self,
        method_name: str,
        parameters: str,
        returns: str,
        specs: str,
        body: str,
    ) -> str:
        return (
            self.validator_template_pure_copy.replace("{method_name}", method_name)
            .replace("{parameters}", parameters or "")
            .replace("{returns}", returns or "")
            .replace("{specs}", specs or "\n")
            .replace(
                "{param_names}",
                self.split_params(parameters),
            )
            .replace("{body}", body)
        )

    def _validators_from_pure(
        self,
        method_name: str,
        parameters: str,
        returns: str,
        specs: str,
        body: str,
    ) -> str:
        return (
            self.validator_template_pure.replace("{method_name}", method_name)
            .replace("{parameters}", parameters or "")
            .replace("{returns}", returns or "")
            .replace("{specs}", specs or "\n")
            .replace(
                "{param_names}",
                self.split_params(parameters),
            )
            .replace("{body}", body)
        )

    def replace_pure(self, code: str, pure_names: list[str]):
        for pure_name in pure_names:
            code = code.replace(pure_name + "(", pure_name + "_copy_pure(")
        return code

    def generate_validators(self, code: str, validate_helpers: bool) -> str:
        pure_methods = list(self.pure_regex.finditer(code))
        methods = list(self.method_regex.finditer(code))

        validators: list[str] = []
        pure_names: list[str] = []

        for pure_match in pure_methods:
            method_name = pure_match.group(1)
            pure_names.append(method_name)

        if self.remove_pure:
            for pure_match in pure_methods:
                method_name, parameters, returns, specs, body = (
                    pure_match.group(1),
                    pure_match.group(2),
                    pure_match.group(3),
                    pure_match.group(4),
                    pure_match.group(5),
                )

                specs = self.replace_pure(specs, pure_names)
                body = self.replace_pure(body, pure_names)

                validators.append(
                    self._validators_from_pure_copy(
                        method_name, parameters, returns, specs, body
                    )
                )

        if validate_helpers:
            for pure_match in pure_methods:
                method_name, parameters, returns, specs, body = (
                    pure_match.group(1),
                    pure_match.group(2),
                    pure_match.group(3),
                    pure_match.group(4),
                    pure_match.group(5),
                )
                validators.append(
                    self._validators_from_pure(
                        method_name, parameters, returns, specs, body
                    )
                )

        for match in methods:
            method_name, parameters, returns, specs = (
                match.group(1),
                match.group(2),
                match.group(3),
                match.group(4),
            )

            if method_name in pure_names:
                continue

            if self.remove_pure:
                specs = self.replace_pure(specs, pure_names)

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
        self, code: str, pure_non_helpers: List[str]
    ) -> Tuple[List[str], str]:
        return [], code

    def find_pure_non_helpers(self, code: str) -> List[str]:
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

    def reset(self):
        self.languages = dict()
        self.regularise = dict()
