from pathlib import Path
from typing import Literal
from typing_extensions import Self
import re
from tqdm import tqdm
from aoc_utils import timing


class Computer:
    def __init__(
        self, registers: dict[Literal["A", "B", "C"], int], instructions: list[int]
    ):
        self.registers = registers
        self.instructions = instructions
        self.pointer = 0
        self.outputs = list()

    @staticmethod
    def literal(operand: int) -> int:
        return operand

    def combo(self, operand: int) -> int:
        if operand <= 3:
            return operand
        if operand > 6:
            raise ValueError
        register = "ABC"[operand - 4]
        return self.registers[register]

    @classmethod
    def from_file(cls, path: Path) -> Self:
        with path.open("r") as fin:
            text = fin.read()
        registers = re.findall(r"Register ([A-C]): (\d+)", text)
        registers = {name: int(value) for name, value in registers}
        operations = list(map(int, re.findall(r"\d+", text.split("\n\n")[-1])))
        return Computer(registers, operations)

    def do(self, instruction: int, operand: int) -> bool:
        if instruction == 0:
            self.registers["A"] = self.registers["A"] // 2 ** self.combo(operand)
        elif instruction == 1:
            self.registers["B"] = self.registers["B"] ^ operand
        elif instruction == 2:
            self.registers["B"] = self.combo(operand) % 8
        elif instruction == 3:
            if self.registers["A"] != 0:
                self.pointer = operand
                return
        elif instruction == 4:
            self.registers["B"] = self.registers["B"] ^ self.registers["C"]
        elif instruction == 5:
            self.outputs.append(self.combo(operand) % 8)
        elif instruction == 6:
            self.registers["B"] = self.registers["A"] // 2 ** self.combo(operand)
        elif instruction == 7:
            self.registers["C"] = self.registers["A"] // 2 ** self.combo(operand)
        else:
            raise ValueError
        self.pointer += 2
        return

    def execute(self, p2: bool = False) -> None:
        while self.pointer < len(self.instructions) - 1:
            opcode, operand = self.instructions[self.pointer : self.pointer + 2]
            self.do(opcode, operand)
            if p2 and self.instructions[: len(self.outputs)] != self.outputs:
                break
        return

    def __str__(self) -> str:
        return "\n".join([str(self.registers), str(self.instructions)])


def part_one(path: Path) -> int:
    computer = Computer.from_file(path)
    computer.execute()
    return ",".join(list(map(str, computer.outputs)))


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def solve(computer: Computer) -> int:
    """
    This solution is heavily linked with the computer program I got.
    I do not know if it generalizes well.
    """
    previous_stack = [0]
    for value in reversed(computer.instructions):
        stack = list()
        for previous_value in previous_stack:
            for digit in range(8):
                a = previous_value * 8 + digit
                computer = Computer({"A": a, "B": 0, "C": 0}, computer.instructions)
                computer.execute()
                if computer.outputs[0] == value:
                    stack.append(a)
        min_stack = min(stack)
        previous_stack = stack
    computer = Computer({"A": min_stack, "B": 0, "C": 0}, computer.instructions)
    computer.execute()
    print(computer.outputs, computer.instructions)
    print(min_stack)
    exit()
    for i in range(8):
        register = {"A": 8**15 * i, "B": 0, "C": 0}
        computer = Computer(register, computer.instructions)
        computer.execute()
        print(i, computer.outputs, computer.instructions)
    exit()
    total = 0
    # for i, digit in enumerate(digits):
    #     total += 8 ** (len(computer.instructions) - 1 - i) * digit
    return total


def part_two(path: Path) -> int:
    computer = Computer.from_file(path)
    a_value = solve(computer)
    computer = Computer({"A": a_value, "B": 0, "C": 0}, computer.instructions)
    computer.execute()
    print(computer.outputs, computer.instructions)
    return a_value
    # computer = Computer({"A": 117440, "B": 0, "C": 0}, [0, 3, 5, 4, 3, 0])
    original_registers = computer.registers
    instructions = computer.instructions
    registers = dict(original_registers)
    registers["A"] = 8**15
    registers["B"] = 0
    for i in range(8):
        registers = dict(original_registers)
        registers["A"] = 8**15 + i
        computer = Computer(registers, instructions)
        computer.execute()
        print(computer.outputs, computer.registers)
    print(instructions)
    exit()
    computer = Computer(registers, [1, 5])
    computer.execute()
    print(computer)
    exit()
    pbar = tqdm()
    for i in count(start=8**15):
        if i % 10**4 == 0:
            pbar.update(10**4)
        registers = {key: val for key, val in original_registers.items()}
        registers["A"] = i
        computer = Computer(registers, instructions)

        computer.execute(p2=True)
        if computer.outputs == computer.instructions:
            break
    return i


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
