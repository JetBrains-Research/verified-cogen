from abc import abstractmethod
from typing import Pattern


class Language:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def generate_validators(self, code: str) -> str: ...


class GenericLanguage(Language):
    method_regex: Pattern[str]
    validator_template: str

    def __init__(self, method_regex: Pattern[str], validator_template: str):
        self.method_regex = method_regex
        self.validator_template = validator_template

    def generate_validators(self, code: str) -> str:
        methods = self.method_regex.finditer(code)

        validators = []

        for match in methods:
            print(match.groups())
            method_name, parameters, returns, specs = (
                match.group(1),
                match.group(2),
                match.group(3),
                match.group(4),
            )

            validators.append(
                self.validator_template.replace("{method_name}", method_name)
                .replace("{parameters}", parameters)
                .replace("{returns}", returns)
                .replace("{specs}", specs)
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


class LanguageDatabase:
    _instance = None
    languages: dict[str, Language] = dict()
    regularise: dict[str, str] = dict()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def add(self, name: str, aliases: list[str], definition: Language):
        self.languages[name] = definition
        self.regularise[name] = name
        for alias in aliases:
            self.regularise[alias] = name

    def get(self, name: str):
        if name not in self.regularise:
            raise ValueError(f"language {name} not found, has it been registered?")
        return self.languages[self.regularise[name]]
