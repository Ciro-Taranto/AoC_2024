from pathlib import Path
from typing import Optional, Sequence
from itertools import product

from aoc_utils import timing

PerimeterSection = list[tuple[float, float]]
Point = tuple[int, int]
Direction = tuple[int, int]

DIRECTIONS = [(0, -1), (1, 0), (-1, 0), (0, 1)]


class Patch:
    def __init__(self, value: str, squares: Sequence[Point]):
        self.value = value
        self.squares = set(squares)

    def __str__(self) -> str:
        return f"Value: {self.value}, area: {self.area}"

    @property
    def area(self) -> int:
        return len(self.squares)

    def get_perimeter(
        self,
    ) -> dict[str, list[Point]]:
        perimeter = {"u": [], "d": [], "l": [], "r": []}
        for sq in self.squares:
            if (sq[0], sq[1] + 1) not in self.squares:
                perimeter["r"].append(sq)
            if (sq[0], sq[1] - 1) not in self.squares:
                perimeter["l"].append(sq)
            if (sq[0] + 1, sq[1]) not in self.squares:
                perimeter["d"].append(sq)
            if (sq[0] - 1, sq[1]) not in self.squares:
                perimeter["u"].append(sq)
        return perimeter

    def split_perimeter_into_lines(
        self,
    ) -> list[PerimeterSection]:
        perimeter = self.get_perimeter()
        continuous_sections = []
        for key in ["l", "r"]:
            vp = set(perimeter[key])
            while vp:
                start = vp.pop()
                section = {start}
                current = start
                while (down := (current[0] + 1, current[1])) in vp:
                    section.add(down)
                    vp.remove(down)
                    current = down
                current = start
                while (up := (current[0] - 1, current[1])) in vp:
                    section.add(up)
                    vp.remove(up)
                    current = up
                continuous_sections.append(section)
        for key in ["u", "d"]:
            hp = set(perimeter[key])
            while hp:
                start = hp.pop()
                section = {start}
                current = start
                while (right := (current[0], current[1] + 1)) in hp:
                    section.add(right)
                    hp.remove(right)
                    current = right
                current = start
                while (left := (current[0], current[1] - 1)) in hp:
                    section.add(left)
                    hp.remove(left)
                    current = left
                continuous_sections.append(section)
        return continuous_sections


class GardenMap:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def __getitem__(self, item: tuple[int, int]) -> Optional[str]:
        if 0 <= item[0] < self.max_y and 0 <= item[1] < self.max_x:
            return self.lines[item[0]][item[1]]
        return None

    def get_patches(self) -> list[tuple[Patch, int]]:
        patches_and_perimeters = []
        to_visit = set(product(range(self.max_y), range(self.max_x)))
        visited = set()
        while to_visit:
            square = to_visit.pop()
            plant = self[square]
            patch = {square}
            frontier = {square}
            visited.add(square)
            perimeter = 0
            while frontier:
                square = frontier.pop()
                for direction in DIRECTIONS:
                    next_square = square[0] + direction[0], square[1] + direction[1]
                    if self[next_square] == plant:
                        if next_square not in visited:
                            frontier.add(next_square)
                            patch.add(next_square)
                            visited.add(next_square)
                            to_visit.remove(next_square)
                    else:
                        perimeter += 1
            patches_and_perimeters.append((Patch(plant, patch), perimeter))
        return patches_and_perimeters


def parse_file(path: Path) -> GardenMap:
    with path.open("r") as fin:
        return GardenMap(fin.read().strip().split("\n"))


def part_one(path: Path) -> int:
    garden_map = parse_file(path)
    patches_and_perimeters = garden_map.get_patches()
    print(
        sum(patch.area for patch, _ in patches_and_perimeters),
        garden_map.max_x * garden_map.max_y,
    )
    return sum(patch.area * perimeter for patch, perimeter in patches_and_perimeters)


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    garden_map = parse_file(path)
    patches_and_perimeters = garden_map.get_patches()
    return sum(
        patch.area * len(patch.split_perimeter_into_lines())
        for patch, _ in patches_and_perimeters
    )


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
