from __future__ import annotations
import copy
from pathlib import Path
from tqdm import tqdm
from itertools import product


from aoc_utils import timing

MIN_X = 0
MAX_X = 130
MIN_Y = 0
MAX_Y = 130

transitions = {"^": ">", "v": "<", ">": "v", "<": "^"}


movements = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def add_direction(
    point: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    return point[0] + direction[0], point[1] + direction[1]


class Map:
    def __init__(self, lines: list[str]):
        self.obstructions = set()
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == "#":
                    self.obstructions.add((i, j))
                if char in movements:
                    self.position = (i, j)
                    self.direction = char
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def add_obstruction(self, obstruction: tuple[int, int]) -> Map:
        new_obstructions = {obstruction}.union(self.obstructions)
        # Note: this must be done properly with a proper init
        new_map = copy.deepcopy(self)
        new_map.obstructions = new_obstructions
        return new_map

    def in_bounds(self, position: tuple[int, int]) -> bool:
        return (
            position[0] >= 0
            and position[0] < self.max_x
            and position[1] >= 0
            and position[1] < self.max_y
        )


def explore(my_map: Map) -> set:
    current = my_map.position
    direction = my_map.direction
    explored = {my_map.position}
    while True:
        next_position = add_direction(current, movements[direction])
        if not my_map.in_bounds(next_position):
            return explored
        if next_position not in my_map.obstructions:
            explored.add(next_position)
            current = next_position
        else:
            direction = transitions[direction]


def has_loop(
    free_spaces: set[tuple[int, int]],
    obstructions: set[tuple[int, int]],
    new_obstruction: tuple[int, int],
    position: tuple[int, int],
    direction: str,
) -> bool:
    current = position
    explored = {(position, direction)}
    free_spaces.remove(new_obstruction)
    while True:
        next_position = (
            current[0] + movements[direction][0],
            current[1] + movements[direction][1],
        )
        if next_position in free_spaces:
            if (next_position, direction) in explored:
                free_spaces.add(new_obstruction)
                return True
            else:
                explored.add((next_position, direction))
                current = next_position
        else:
            if next_position in obstructions or next_position == new_obstruction:
                direction = transitions[direction]
            else:
                free_spaces.add(new_obstruction)
                return False


def find_loop_makers(my_map: Map) -> set[tuple[int, int]]:
    free_spaces = set(product(range(0, MAX_X), range(0, MAX_Y))).difference(
        my_map.obstructions
    )
    explored = explore(my_map)
    valid = set()
    for new_obstruction in tqdm(explored):
        if has_loop(
            free_spaces,
            my_map.obstructions,
            new_obstruction,
            my_map.position,
            my_map.direction,
        ):
            valid.add(new_obstruction)
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
