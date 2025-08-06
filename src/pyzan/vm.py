from pyzan.db import Database
from pyzan.log import Logger
from pyzan.serialization import Serializable
from pyzan.op_code import OpCode
from pyzan.file_handler import open_file

from typing import List, TextIO

vm_log = Logger(module="VM", log_file="logs/vm.log")


class VirtualMachine(Serializable):
    def __init__(self, id: str):
        self.id = id

        self.stack: List[OpCode] = []
        self.instruction_pointer: int = 0
        self.running: bool = True

        self.state_db: Database = None
        self.opened_files: List[TextIO] = []

        self.opened_file: TextIO = None

    def init(self):
        self.state_db = Database("vm_state.db")

    def run(self, program, type="default"):
        while self.running and self.instruction_pointer < len(program):
            instruction = program[self.instruction_pointer]
            op = instruction[0]

            if type == "debug":
                vm_log.info(f"Executing OpCode => {op}")

            if op == OpCode.OPEN:
                filename, mode = instruction[1], instruction[2]
                try:
                    self.opened_file = open(filename, mode)
                    self.opened_files.append(self.opened_file)
                    if type == "debug":
                        vm_log.info(f"Opened file '{filename}' in mode '{mode}'")
                except Exception as e:
                    vm_log.info(f"Failed to open file {e}")
                    self.running = False
            elif op == OpCode.WRITE:
                data = instruction[1]
                if self.opened_file:
                    self.opened_file.write(data)
            elif op == OpCode.READ:
                filename = instruction[1]
                if self.opened_file:
                    self.opened_file.close()
                    self.opened_file = open(filename, "r")
                else:
                    self.opened_file = open(filename, "r")
                print(f"READ {filename}: {self.opened_file.read()}")
            elif op == OpCode.END:
                self.running = False
            else:
                raise Exception(f"Unknown OpCode: {op}")

            self.instruction_pointer += 1

        if self.opened_file:
            self.opened_file.close()

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

    def restore_machine(self, snapshot):
        """TODO: Implement"""
        pass