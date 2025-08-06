from pyzan.vm import VirtualMachine
from pyzan.op_code import OpCode
from pyzan.vm_id import VirtualMachineID
from pyzan.parser import FileParser

if __name__ == "__main__":
    prog = FileParser.parse_file(file="example/example.zan")

    vm = VirtualMachine(VirtualMachineID.get())

    vm.init()

    vm.run(program=prog, type="debug")