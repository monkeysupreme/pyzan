from pyzan.vm import VirtualMachine
from pyzan.op_code import OpCode
from pyzan.vm_id import VirtualMachineID

if __name__ == "__main__":
    prog = [
        (OpCode.PUSH, 10),
        (OpCode.PUSH, 10),
        (OpCode.ADD,),
        (OpCode.PRINT,),
        (OpCode.END,)
    ]

    vm = VirtualMachine(VirtualMachineID.get())

    vm.init()
    vm.run(program=prog)