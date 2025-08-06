from enum import Enum, auto


class OpCode(Enum):
    OPEN    = auto()
    WRITE   = auto()
    READ    = auto()
    END     = auto()