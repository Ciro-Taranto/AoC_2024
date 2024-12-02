from pathlib import Path

from aoc_utils import timing


def parse_file(path: Path) -> list[tuple[int, ...]]:
    numbers = []
    with path.open("r") as fin:
        for line in fin.readlines():
            numbers.append(tuple([int(val) for val in line.strip().split(" ")]))
    return numbers


def all_increasing(line: tuple[int, int, int, int, int]) -> bool:
    return all(r > l for l, r in zip(line[:-1], line[1:]))


def all_diff_are_small(line: tuple[int, int, int, int, int]) -> bool:
    return all(r - l <= 3 for l, r in zip(line[:-1], line[1:]))


def is_line_safe_increasing(line: tuple[int, ...]) -> bool:
    return all_increasing(line) and all_diff_are_small(line)


def is_line_safe(line: tuple[int, ...]) -> bool:
    return is_line_safe_increasing(line) or is_line_safe_increasing(
        list(reversed(line))
    )


def is_line_safe_with_dampening(line: tuple[int, ...]) -> bool:
    if is_line_safe(line):
        return True
    # brute force because it is early in the morning
    for i in range(len(line)):
        new_line = list(line)
        new_line.pop(i)
        if is_line_safe(new_line):
            return True
    return False


def part_one(path: Path) -> int:
    numbers = parse_file(path)
    return sum([is_line_safe(line) for line in numbers])


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    lines = parse_file(path)
    return sum([is_line_safe_with_dampening(line) for line in lines])


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
