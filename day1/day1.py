from pathlib import Path
from collections import Counter

from aoc_utils import timing


def parse_file(path: Path) -> tuple[list[int, int]]:
    first_list = []
    second_list = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            n1, n2 = line.strip().split("  ")
            first_list.append(int(n1))
            second_list.append(int(n2))
    return first_list, second_list


def part_one(path: Path) -> int:
    first_list, second_list = parse_file(path)
    return sum(abs(b - a) for a, b in zip(sorted(first_list), sorted(second_list)))


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    first_list, second_list = parse_file(path)
    counts = Counter(second_list)
    return sum(a * counts.get(a, 0) for a in first_list)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
