from pathlib import Path
import numpy as np
from typing import Optional
from tqdm import tqdm
import re

from aoc_utils import timing


class ClawMachine:
    A_COST = 3
    B_COST = 1

    def __init__(
        self, x_a: int, y_a: int, x_b: int, y_b: int, x_prize: int, y_prize: int
    ):
        self.x_a = x_a
        self.y_a = y_a
        self.x_b = x_b
        self.y_b = y_b
        self.x_prize = x_prize
        self.y_prize = y_prize

    def solve(self, showsol: bool = False) -> Optional[int]:
        possible_solutions = []
        for push_a in range(100):
            tot_x_a = self.x_a * push_a
            tot_y_a = self.y_a * push_a
            miss_x = self.x_prize - tot_x_a
            miss_y = self.y_prize - tot_y_a
            if miss_x < 0 or miss_y < 0:
                break
            if miss_x % self.x_b == 0:
                push_b = miss_x // self.x_b
                if push_b * self.y_b == miss_y:
                    possible_solutions.append((push_a, push_b))
        if showsol:
            print(possible_solutions)
        if possible_solutions:
            return min(
                self.A_COST * push_a + self.B_COST * push_b
                for push_a, push_b in possible_solutions
            )
        return 0

    def mathsolve(self, showsol: bool = False) -> Optional[int]:
        """
        We solve these two equations in two unknwons:
        p_a * a_x + p_b * b_x = x
        p_a * a_y + p_b * b_y = y
        """
        sol = np.linalg.solve(
            np.array([[self.x_a, self.x_b], [self.y_a, self.y_b]]),
            np.array([self.x_prize, self.y_prize]),
        )

        if (
            np.allclose(sol - np.round(sol, 0), np.zeros_like(sol), atol=1e-4)
            and (sol >= 0).all()
        ):
            if showsol:
                print(sol.astype(int), sol - np.round(sol))

            coeffs = np.array([self.A_COST, self.B_COST])
            return np.dot(coeffs, np.round(sol).astype(int))
        return 0


def parse_file(path: Path) -> list[ClawMachine]:
    with path.open("r") as fin:
        matches = re.findall(
            r"Button A: X\+(\d+), Y\+(\d+).*\nButton B: X\+(\d+), Y\+(\d+).*\nPrize: X\=(\d+), Y=(\d+)",
            fin.read(),
        )
    return [ClawMachine(*list(map(int, match))) for match in matches]


def part_one(path: Path) -> int:
    claw_machines = parse_file(path)
    total = 0
    for i, claw_machine in enumerate(tqdm(claw_machines)):
        tokens = claw_machine.solve()
        print(f"Claw Machine {i}: {tokens}")
        if tokens is not None:
            total += tokens
    return total


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    claw_machines = parse_file(path)
    offset = 10000000000000
    for claw_machine in claw_machines:
        claw_machine.x_prize += offset
        claw_machine.y_prize += offset

    return int(sum(claw_machine.mathsolve(True) for claw_machine in claw_machines))


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
