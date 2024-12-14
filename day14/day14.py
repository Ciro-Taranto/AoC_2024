from pathlib import Path
from typing import TypeAlias
from itertools import product
from typing_extensions import Self
import re
from tqdm import tqdm

from aoc_utils import timing


Point: TypeAlias = tuple[int, int]
Velocity: TypeAlias = tuple[int, int]


class Robot:
    def __init__(self, position: Point, velocity: Velocity):
        self.position = position
        self.velocity = velocity

    def one_step(self, max_x: int, max_y: int) -> Self:
        next_x = (self.position[0] + self.velocity[0]) % max_x
        next_y = (self.position[1] + self.velocity[1]) % max_y
        self.position = (next_x, next_y)
        return self


class RobotMap:
    def __init__(self, robots: list[Robot], max_x: int, max_y: int):
        self.robots = robots
        self.max_x = max_x
        self.max_y = max_y

    def do_steps(self, n_steps: int, visualize: bool = True) -> None:
        for step in tqdm(range(n_steps)):
            for robot in self.robots:
                robot.one_step(self.max_x, self.max_y)
            max_strings_lengths = self.get_contiguous_strings()
            do_visualize = sorted(max_strings_lengths.values(), reverse=True)[2] >= 5
            if visualize and do_visualize:
                print("##################")
                print(f"Step: {step}")
                print(self)

    def count_in_quadrants(self) -> dict[tuple[bool, bool], int]:
        quadrant_counts = {
            (up, left): 0 for up, left in product([True, False], [True, False])
        }
        x_division = (self.max_x - 1) // 2
        y_division = (self.max_y - 1) // 2
        for robot in self.robots:
            x, y = robot.position
            if x != x_division and y != y_division:
                quadrant_counts[
                    robot.position[0] > x_division, robot.position[1] > y_division
                ] += 1
        return quadrant_counts

    def robot_positions(self) -> set[Point]:
        positions = set()
        for robot in self.robots:
            positions.add(robot.position)
        return positions

    def vertically_symmetric(self, symmetry_fraction: float = 0.2) -> bool:
        positions = self.robot_positions()
        n_asym = 0
        for x, y in positions:
            if ((self.max_x - 1 - x), y) not in positions:
                n_asym += 1
        return (n_asym / len(positions)) < (1 - symmetry_fraction)

    def robots_on_lines(self) -> dict[int, set[int]]:
        roboset = set([robot.position for robot in self.robots])
        robots_on_lines = {i: set() for i in range(self.max_y)}
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in roboset:
                    robots_on_lines[y].add(x)
        return robots_on_lines

    def get_contiguous_strings(self) -> dict[int, int]:
        robots_on_lines = self.robots_on_lines()
        max_strings_length = dict()
        for y, robots_on_line in robots_on_lines.items():
            current_length = 0
            max_length = 0
            for x in range(self.max_x):
                if x in robots_on_line:
                    current_length += 1
                else:
                    max_length = max(current_length, max_length)
                    current_length = 0
            max_strings_length[y] = max_length
        return max_strings_length

    def __str__(self):
        occupations = {
            (i, j): 0 for i, j in product(range(self.max_x), range(self.max_y))
        }
        for robot in self.robots:
            occupations[(robot.position[0], robot.position[1])] += 1
        lines = []
        for y in range(self.max_y):
            line = []
            for x in range(self.max_x):
                occ = occupations[(x, y)]
                line.append(str(occ) if occ > 0 else ".")
            lines.append("".join(line))
        return "\n".join(lines)


def parse_file(path: Path) -> RobotMap:
    with path.open("r") as fin:
        input_text = fin.read()
    robots = []
    for match in re.findall("p=(-*\d+),(-*\d+) v=(-*\d+),(-*\d+)", input_text):
        x, y, vx, vy = list(map(int, match))
        robots.append(Robot((x, y), (vx, vy)))
    if "example" in path.name:
        max_x, max_y = 11, 7
    else:
        max_x, max_y = 101, 103
    return RobotMap(robots, max_x, max_y)


def part_one(path: Path) -> int:
    robot_map = parse_file(path)
    robot_map.do_steps(100, visualize=False)
    quadrant_counts = robot_map.count_in_quadrants()
    values = list(quadrant_counts.values())
    ret = values[0]
    for val in values[1:]:
        ret *= val
    return ret


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    robot_map = parse_file(path)
    robot_map.do_steps(10**9, visualize=True)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
