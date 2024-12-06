from __future__ import annotations
import copy
from pathlib import Path
from dataclasses import dataclass
from tqdm import tqdm
from itertools import product

from aoc_utils import timing


transitions = {"^": ">", "v": "<", ">": "v", "<": "^"}


@dataclass
class Direction:
    y: int
    x: int


movements = {
    "^": Direction(-1, 0),
    "v": Direction(1, 0),
    ">": Direction(0, 1),
    "<": Direction(0, -1),
}


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, direction: Direction) -> Point:
        return Point(self.y + direction.y, self.x + direction.x)


class Map:
    def __init__(self, lines: list[str]):
        self.obstructions = set()
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == "#":
                    self.obstructions.add(Point(i, j))
                if char in movements:
                    self.position = Point(i, j)
                    self.direction = char
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def add_obstruction(self, obstruction: Point) -> Map:
        new_obstructions = {obstruction}.union(self.obstructions)
        # Note: this must be done properly with a proper init
        new_map = copy.deepcopy(self)
        new_map.obstructions = new_obstructions
        return new_map

    def in_bounds(self, position: Point) -> bool:
        return (
            position.x >= 0
            and position.x < self.max_x
            and position.y >= 0
            and position.y < self.max_y
        )


def explore(my_map: Map) -> set:
    current = my_map.position
    direction = my_map.direction
    explored = {my_map.position}
    while True:
        next_position = current + movements[direction]
        if not my_map.in_bounds(next_position):
            return explored
        if next_position not in my_map.obstructions:
            explored.add(next_position)
            current = next_position
        else:
            direction = transitions[direction]


def has_loop(my_map: Map) -> bool:
    current = my_map.position
    direction = my_map.direction
    explored = {(my_map.position, direction)}
    while True:
        next_position = current + movements[direction]
        if not my_map.in_bounds(next_position):
            return False
        if (next_position, direction) in explored:
            return True
        if next_position not in my_map.obstructions:
            explored.add((next_position, direction))
            current = next_position
        else:
            direction = transitions[direction]


def find_loop_makers(my_map: Map) -> set[Point]:
    explored = explore(my_map)
    valid = set()
    # for i, j in tqdm(product(range(my_map.max_x), range(my_map.max_y))):
    # new_obstruction = Point(j, i)
    for new_obstruction in tqdm(explored):
        if new_obstruction in my_map.obstructions or new_obstruction == my_map.position:
            continue
        new_map = my_map.add_obstruction(new_obstruction)
        if has_loop(new_map):
            valid.add(new_map)
    return valid


def parse_file(path: Path) -> Map:
    with path.open("r") as fin:
        lines = fin.readlines()
    return Map(lines)


def part_one(path: Path) -> int:
    my_map = parse_file(path)
    explored = explore(my_map)
    return len(explored)


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    my_map = parse_file(path)
    valid = find_loop_makers(my_map)
    return len(valid)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
