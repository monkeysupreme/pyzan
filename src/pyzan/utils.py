from pyzan.db import VirtualMachineMemoryStorage
from pyzan.vm import vm_log


def run_virtual_machine_batch(vmm: VirtualMachineMemoryStorage, programs):
    if len(programs) != len(vmm.machines):
        vm_log.error("Program to machine ratio mismatch")
        return

    for program in programs:
        for machine_id, machine in vmm.machines.items():
            machine.run(program=program, type="default")