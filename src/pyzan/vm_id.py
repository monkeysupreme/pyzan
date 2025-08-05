import uuid


class VirtualMachineID:
    @staticmethod
    def get() -> str:
        return str(uuid.uuid4().hex)