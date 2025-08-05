from pyzan.db import Database
from pyzan.log import Logger
from pyzan.serialization import Serializable
from pyzan.op_code import OpCode

from typing import List


vm_log = Logger(module="VM", log_file="logs/vm.log")


class VirtualMachine(Serializable):
    def __init__(self, id: str):
        self.id = id

        self.stack: List[OpCode] = []
        self.instruction_pointer: int = 0
        self.running: bool = True

        self.state_db: Database = None

    def init(self):
        self.state_db = Database("vm_state.db")

    def run(self, program, mode="default"):
        while self.running and self.instruction_pointer < len(program):
            instruction = program[self.instruction_pointer]
            op = instruction[0]

            if mode == "debug":
                vm_log.info(f"Executing OpCode => {op}")

            if op == OpCode.PUSH:
                self.stack.append(instruction[1])
            elif op == OpCode.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif op == OpCode.PRINT:
                print(self.stack[-1])
            elif op == OpCode.END:
                self.running = False
            else:
                raise Exception(f"Unknown OpCode: {op}")

            self.instruction_pointer += 1

    def save_machine_state(self) -> None:
        if not self.state_db:
            print("VirtualMachine.save_machine_state(...): State DB is not connected")
            return

        self.state_db.insert(self.id, self.serialize())

    def get_machine_state(self, machine_id: str):
        if not self.state_db:
            print("VirtualMachine.get_machine_state(...): State DB is not connected")
            return

        serialized_machine = self.state_db.query(machine_id)
        if serialized_machine is None:
            print(f"No saved state found for VM ID: {machine_id}")
            return None

        return self.deserialize(serialized_machine)

    def dump_machine_state(self, machine_id: str) -> None:
        machine = self.get_machine_state(machine_id)
        print(machine.serialize())