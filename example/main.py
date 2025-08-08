from pyzan.parser import FileParser
from pyzan.vm import VirtualMachine
from pyzan.vm_id import VirtualMachineID

if __name__ == "__main__":
    vm = VirtualMachine(VirtualMachineID.get())
    vm.init()
    parsed_vm_prog_file = FileParser.parse_file(file="example/example.pzn")
    vm.run(program=parsed_vm_prog_file, type="debug")