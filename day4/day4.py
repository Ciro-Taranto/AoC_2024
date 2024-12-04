from pathlib import Path
import re
from collections import defaultdict

from aoc_utils import timing


def parse_file(path: Path) -> str:
    with path.open("r") as fin:
        return fin.read()


def find_on_line(line: str) -> int:
    # Yes, it could be done with a single regex,
    # but one would have to take care of the overlap
    return len(re.findall(r"XMAS", line)) + len(re.findall(r"SAMX", line))


def get_vertical_lines(lines: list[str]) -> list[str]:
    vertical_lines = defaultdict(list)
    for line in lines:
        for j, char in enumerate(line):
            vertical_lines[j].append(char)
    vertical_lines = ["".join(line) for line in vertical_lines.values()]
    return vertical_lines


def get_diagonal_lines(lines: list[str]) -> list[str]:
    number_of_rows = len(lines)
    number_of_columns = (s := set(len(line) for line in lines)).pop()
    if s:
        raise ValueError("Not rectangular?")
    if number_of_columns != number_of_rows:
        raise ValueError("Not square?")
    n = number_of_rows
    diagonal_lines = []
    for offset in range(-n, n):
        diagonal_line = []
        for r in range(n):
            c = offset + r
            if c < 0 or c >= n:
                continue
            diagonal_line.append(lines[r][c])
        diagonal_lines.append(diagonal_line)
    return ["".join(line) for line in diagonal_lines]


def part_one(path: Path) -> int:
    text = parse_file(path)
    lines = text.split("\n")
    horizontal = sum(map(find_on_line, lines))
    vertical_lines = get_vertical_lines(lines)
    vertical = sum(map(find_on_line, vertical_lines))
    diagonal_lines = get_diagonal_lines(lines)
    diagonal = sum(map(find_on_line, diagonal_lines))
    other_diagonal_lines = get_diagonal_lines(
        ["".join(reversed(line)) for line in lines]
    )
    other_diagonal = sum(map(find_on_line, other_diagonal_lines))
    return horizontal + vertical + diagonal + other_diagonal


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def scan_x_mas(lines: list[str]) -> int:
    matches = 0
    # Yes, we could use numpy and call it a day
    for i in range(len(lines) - 2):
        triplet = lines[i : i + 3]
        matches += _scan_on_triplet(triplet)
    return matches


def _scan_on_triplet(lines: list[str]) -> int:
    n = len(lines[0])
    matches = 0
    for i in range(n - 2):
        matches += _is_a_match([line[i : i + 3] for line in lines])
    return matches


def get_diagonal(lines: list[str], main: bool = True):
    if not main:
        lines = ["".join(reversed(line)) for line in lines]
    return "".join(lines[i][i] for i in range(len(lines)))


def _is_a_match(lines: list[str]) -> bool:
    return get_diagonal(lines) in {"MAS", "SAM"} and get_diagonal(
        lines, main=False
    ) in {"MAS", "SAM"}


def part_two(path: Path) -> int:
    lines = parse_file(path).split("\n")
    return scan_x_mas(lines)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
