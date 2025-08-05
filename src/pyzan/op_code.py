from enum import Enum, auto


class OpCode(Enum):
    PUSH = auto()
    ADD = auto()
    PRINT = auto()
    END = auto()