from abc import abstractmethod
from typing import Pattern, Any


class Language:
    _instance = None
    simple_comment: str

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]): ...

    @abstractmethod
    def generate_validators(self, code: str) -> str: ...

    @abstractmethod
    def remove_asserts_and_invariants(self, code: str) -> str: ...


class GenericLanguage(Language):
    method_regex: Pattern[str]
    validator_template: str
    assert_invariant_patterns: list[str]
    inline_assert_comment: str

    def __init__(  # type: ignore
        self,
        method_regex: Pattern[str],
        validator_template: str,
        assert_invariants_pattern: list[str],
        inline_assert_comment: str,
        simple_comment: str,
    ):
        self.simple_comment = simple_comment
        self.method_regex = method_regex
        self.validator_template = validator_template
        self.assert_invariant_patterns = assert_invariants_pattern
        self.inline_assert_comment = inline_assert_comment

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

        return "\n".join(validators)

    def remove_asserts_and_invariants(self, code: str) -> str:
        import re

        combined_pattern = "|".join(self.assert_invariant_patterns)
        cleaned_code = re.sub(combined_pattern, "", code, flags=re.DOTALL)
        cleaned_code = re.sub(r"\n\s*\n", "\n", cleaned_code)
        lines = cleaned_code.split("\n")
        lines = [line for line in lines if self.inline_assert_comment not in line]
        return "\n".join(lines).strip()


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
