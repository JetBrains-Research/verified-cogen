from enum import Enum


class Modes(Enum):
    REGEX = 'regex', False
    LLM = 'llm', False
    LLM_SINGLE_STEP = 'llm-single-step', True
    DAFNYBENCH = 'dafnybench', True

    def __new__(cls, id, is_singlestep):
        obj = object.__new__(cls)
        obj._value_ = id
        obj.is_singlestep = is_singlestep
        return obj

    def __repr__(self):
        return self.value


VALID_MODES = [m.name for m in Modes]


def precheck(prg, mode):
    """Precheck that the program can be processed in the given mode before any LLM invocations"""
    while_count = prg.count("while")
    if while_count == 0:
        raise ValueError("No loops in program")
    if mode == Modes.REGEX:
        if while_count > 1:
            raise ValueError("Multiple loops in program, not supported in regex mode")