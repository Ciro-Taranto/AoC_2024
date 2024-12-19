from pathlib import Path
from functools import partial
from tqdm import tqdm
from collections import defaultdict

from aoc_utils import timing


def parse_file(path: Path) -> tuple[list[str], list[str]]:
    with path.open("r") as fin:
        towels, patterns = fin.read().strip().split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.split("\n")
    return towels, patterns


def solve(pattern: str, towels: list[str]) -> bool:
    towels = [towel for towel in towels if towel in pattern]
    queue = {pattern}
    visited = set()
    while queue:
        sp = queue.pop()
        if sp == "":
            return True
        visited.add(sp)
        for towel in towels:
            if sp.startswith(towel):
                nsp = sp[len(towel) :]
                if nsp not in visited:
                    queue.add(nsp)
    return False


def solve_p2(pattern: str, towels_by_length: dict[int, set[str]]) -> dict[int, int]:
    possibilities = defaultdict(int)
    possibilities[0] = 1
    for i in range(0, len(pattern)):
        for l, towels in towels_by_length.items():
            if pattern[i : i + l] in towels:
                possibilities[i + l] += possibilities.get(i, 0)
    return possibilities


def part_one(path: Path) -> int:
    towels, patterns = parse_file(path)
    f = partial(solve, towels=towels)
    return sum(map(f, tqdm(patterns)))


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    towels, patterns = parse_file(path)
    towels_by_length = defaultdict(set)
    for towel in towels:
        towels_by_length[len(towel)].add(towel)
    towels = dict(sorted(towels_by_length.items(), key=lambda k: k[0]))
    return sum(
        solve_p2(pattern, towels_by_length).get(len(pattern), 0) for pattern in patterns
    )


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
