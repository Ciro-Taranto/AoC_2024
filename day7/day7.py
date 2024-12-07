from pathlib import Path
from tqdm import tqdm

from aoc_utils import timing

Calibrations = list[tuple[int, list[int]]]


def parse_file(path: Path) -> Calibrations:
    calibrations = []
    with path.open("r") as fin:
        for line in fin.readlines():
            key, vals = line.split(":")
            vals = list(map(int, vals.strip().split(" ")))
            calibrations.append((int(key), vals))
    return calibrations


def get_next(val1: int, val2: int, part2: bool = False) -> tuple[int, ...]:
    if not part2:
        return val1 + val2, val1 * val2
    else:
        concatenated = int("".join([str(val1), str(val2)]))
        return concatenated, val1 + val2, val1 * val2


def get_valid_contribution(total: int, factors: list[int], part2: bool = False) -> bool:
    current = factors[0]
    queue = [current]
    for right in factors[1:]:
        next_queue = []
        for left in queue:
            vals = get_next(left, right, part2)
            for val in vals:
                if val <= total:
                    next_queue.append(val)
        queue = next_queue
    return total * int(total in queue)


def part_one(path: Path) -> int:
    calibrations = parse_file(path)
    total = 0
    for left, right in tqdm(calibrations):
        total += get_valid_contribution(left, right)
    return total


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    calibrations = parse_file(path)
    total = 0
    for left, right in tqdm(calibrations):
        if get_valid_contribution(left, right, part2=True):
            total += left
    return total


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
