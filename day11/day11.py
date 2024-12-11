from pathlib import Path
from typing import Optional
from tqdm import tqdm
from collections import defaultdict, Counter

from aoc_utils import timing


# Let us try to see if it is possible to cache.
# Considering that all the numbers are multiplied by
# 2024 it might make sense
cache = {}


def parse_file(path: Path) -> list[int]:
    with path.open("r") as fin:
        return list(map(int, fin.read().strip().split(" ")))


def split(n: int) -> Optional[list[int]]:
    s = str(n)
    if len(s) % 2 == 0:
        return [int(s[: len(s) // 2]), int(s[len(s) // 2 :])]
    return None


def cached_split(n: int, N: int) -> dict[int, int]:
    if N < 1:
        raise ValueError
    if (n, N) in cache:
        return cache[(n, N)]
    if N == 1:
        cache[(n, N)] = Counter(apply_rules(n))
    else:
        numbers = defaultdict(int)
        for val, occurrences in cached_split(n, 1).items():
            for nn, vv in cached_split(val, N - 1).items():
                numbers[nn] += vv * occurrences
        cache[(n, N)] = numbers
    return cache[(n, N)]


def apply_rules(n: int) -> list[int]:
    if n == 0:
        return [1]
    if (splitted := split(n)) is not None:
        return splitted
    return [n * 2024]


def part_one(path: Path) -> int:
    numbers = parse_file(path)
    for _ in tqdm(range(25)):
        new_numbers = []
        for n in numbers:
            new_numbers.extend(apply_rules(n))
        numbers = new_numbers
    return len(new_numbers)


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    numbers = parse_file(path)
    total_length = 0
    for n in tqdm(numbers):
        total_length += sum(cached_split(n, 75).values())
    return total_length


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
