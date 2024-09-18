from enum import Enum


class Mode(Enum):
    REGEX = "regex"
    LLM = "llm"
    LLM_SINGLE_STEP = "llm-single-step"

    def __new__(cls, id: str):
        obj = object.__new__(cls)
        obj._value_ = id
        return obj

    def __repr__(self):
        return self.value


VALID_MODES = [m.name for m in Mode]
