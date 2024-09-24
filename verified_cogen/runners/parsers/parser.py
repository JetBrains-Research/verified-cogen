from abc import abstractmethod
from typing import Any

class Parser:
    _instance = None

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]): ...

    @abstractmethod
    def parse(self, text: str) -> str: ...

class ParserDatabase:
    _instance = None
    parsers: dict[str, Parser] = dict()

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def register(self, name: str, definition: Parser):
        self.parsers[name] = definition

    def get(self, name: str):
        if name not in self.parsers:
            raise ValueError(f"parser {name} not found, has it been registered?")
        return self.parsers[name]
