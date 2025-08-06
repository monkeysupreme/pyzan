from pyzan.op_code import OpCode


class FileParser:
    @staticmethod
    def parse_line(line: str):
        parts = line.strip().split()
        if not parts:
            return None

        op_str = parts[0].upper()
        args = parts[1:]

        try:
            op = OpCode[op_str]
        except KeyError:
            raise ValueError(f"Unknown OpCode: {op_str}")

        if op == OpCode.OPEN:
            if len(args) != 2:
                raise ValueError("OPEN requires 2 arguments")
            return op, args[0], args[1]
        else:
            return (op,)

    @staticmethod
    def parse_file(file: str):
        program = []
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                instruction = FileParser.parse_line(line)
                if instruction:
                    program.append(instruction)
        return program