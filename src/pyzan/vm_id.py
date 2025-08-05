import uuid


class VirtualMachineID:
    def __str__(self):
        return uuid.uuid4().hex()