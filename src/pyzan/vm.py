from pyzan.serialization import Serializable
from vm_id import VirtualMachineID
from op_code import OpCode

from typing import List


class VirtualMachine(Serializable):
    def __init__(self, id: VirtualMachineID):
        self.id = id

        self.stack: List[OpCode] = []
        self.instruction_pointer: int = 0
        self.running: bool = True

    def snapshot_state(self):
        pass

    def run(self):
        pass
