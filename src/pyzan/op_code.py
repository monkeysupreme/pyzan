from enum import Enum, auto


class OpCode(Enum):
    OPEN      = auto()
    WRITE     = auto()
    WRITEMANY = auto()
    READ      = auto()
    END       = auto()