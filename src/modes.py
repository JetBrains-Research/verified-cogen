from enum import Enum


class Mode(Enum):
    REGEX = "regex", False
    LLM = "llm", False
    LLM_SINGLE_STEP = "llm-single-step", True
    is_singlestep: bool

    def __new__(cls, id, is_singlestep):
        obj = object.__new__(cls)
        obj._value_ = id
        obj.is_singlestep = is_singlestep
        return obj

    def __repr__(self):
        return self.value


VALID_MODES = [m.name for m in Mode]
