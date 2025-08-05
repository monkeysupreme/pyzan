import sqlite3
import os
from operator import truediv

from typing import List

from vm import VirtualMachine


class MachineDatabase(sqlite3.Connection):
    def __init__(self, file: str) -> None:
        super().__init__(database=file)
        self.file = file

        self.is_new: bool = False

        if not os.path.isfile(file):
            self.is_new = True

        if self.is_new:
            self.execute("CREATE TABLE vm_state (machine_id, serialized_machine);")

    def insert_machine(self, virtual_machine: VirtualMachine) -> None:
        self.execute("INSERT INTO vm_state (machine_id, serialized_machine) VALUES ('{}', {});",
                     virtual_machine.id, virtual_machine.serialize())

    def query_machine(self, machine_id) -> VirtualMachine:
        for row in self.execute(
            "SELECT serialized_machine FROM vm_state WHERE machine_id = '{}';",
            machine_id,
        ):
            serialized_machine = row

        machine = VirtualMachine.deserialize(serialized_machine)

        return machine

    def delete_machine(self, machine_id) -> None:
        self.execute(
            "DELETE FROM vm_state WHERE machine_id = '{}'",
            machine_id,
        )