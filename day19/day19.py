from pathlib import Path
from collections import defaultdict

from aoc_utils import timing


def parse_file(path: Path) -> tuple[dict[int, set[str]], list[str]]:
    with path.open("r") as fin:
        towels, patterns = fin.read().strip().split("\n\n")
    towels_by_length = defaultdict(set)
    for towel in towels.split(", "):
        towels_by_length[len(towel)].add(towel)
    patterns = patterns.split("\n")
    return towels_by_length, patterns


def solve_p2(pattern: str, towels_by_length: dict[int, set[str]]) -> dict[int, int]:
    possibilities = defaultdict(int, {0: 1})
    possibilities[0] = 1
    for i in range(0, len(pattern)):
        for l, towels in towels_by_length.items():
            if pattern[i : i + l] in towels:
                possibilities[i + l] += possibilities.get(i, 0)
    return possibilities


def part_one_and_two(path: Path) -> int:
    towels_by_length, patterns = parse_file(path)
    s = [solve_p2(pattern, towels_by_length)[len(pattern)] for pattern in patterns]
    print(sum(v > 0 for v in s))
    print(sum(s))


with timing():
    part_one_and_two(Path(__file__).parent / "input.txt")
