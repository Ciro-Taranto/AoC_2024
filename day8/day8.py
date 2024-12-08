from pathlib import Path
from collections import defaultdict
from itertools import product, count

from aoc_utils import timing

Antennas = dict[str, list[tuple[int, int]]]
Point = tuple[int, int]


def parse_file(path: Path) -> tuple[Antennas, int, int]:
    with path.open("r") as fin:
        text = fin.read()
    antennas = defaultdict(list)
    for i, line in enumerate(lines := text.split("\n")):
        for j, char in enumerate(line.strip()):
            if char != ".":
                antennas[char].append((j, i))
    max_x = len(lines[0])
    max_y = len(lines)
    print(max_x, max_y)
    return antennas, max_x, max_y


def find_pair_resonances(
    first: Point, second: Point, max_x: int, max_y: int, part2: bool = False
) -> set[Point]:
    resonances = set()
    diff = second[0] - first[0], second[1] - first[1]
    iterator = count() if part2 else range(2, 3)
    for i in iterator:
        resonance = first[0] + i * diff[0], first[1] + i * diff[1]
        if 0 <= resonance[0] < max_x and 0 <= resonance[1] < max_y:
            resonances.add(resonance)
        else:
            break
    for i in iterator:
        resonance = second[0] - i * diff[0], second[1] - i * diff[1]
        if 0 <= resonance[0] < max_x and 0 <= resonance[1] < max_y:
            resonances.add(resonance)
        else:
            break
    return resonances


def find_class_resonances(
    points: list[Point], max_x: int, max_y: int, part2: bool = False
) -> set[Point]:
    resonances = set()
    for first, second in product(points, points):
        if first == second:
            continue
        resonances = resonances.union(
            find_pair_resonances(first, second, max_x, max_y, part2)
        )
    return resonances


def find_all_resonances(
    antennas: Antennas, max_x: int, max_y: int, part2: bool = False
):
    resonances = set()
    for _, points in antennas.items():
        resonances = resonances.union(
            find_class_resonances(points, max_x, max_y, part2)
        )
    return resonances


def print_resonances(resonances: set[Point], max_x: int, max_y: int) -> None:
    lines = []
    for i in range(max_y):
        line = []
        for j in range(max_x):
            char = "." if (j, i) not in resonances else "#"
            line.append(char)
        line = "".join(line)
        lines.append(line)
    lines = "\n".join(lines)
    print(lines)


def part_one(path: Path) -> int:
    antennas, max_x, max_y = parse_file(path)
    resonances = find_all_resonances(antennas, max_x, max_y, part2=False)
    return len(resonances)


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    antennas, max_x, max_y = parse_file(path)
    resonances = find_all_resonances(antennas, max_x, max_y, part2=True)
    return len(resonances)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
