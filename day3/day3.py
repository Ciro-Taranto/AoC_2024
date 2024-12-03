from pathlib import Path
import re

from aoc_utils import timing


def parse_file(path: Path) -> str:
    with path.open("r") as f:
        text = f.read()
    return text


def split_by_do_or_dont(text: str) -> list[str]:
    "return the sequences that should be activated only"
    split_by_dont = text.split("don't()")
    valid_sequences = [split_by_dont.pop(0)]
    for sequence in split_by_dont:
        split_by_do = sequence.split("do()")
        valid_sequences.extend(split_by_do[1:])
    return valid_sequences


def execute_mul(text: str) -> int:
    pattern = pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    operations = re.findall(pattern, text)
    return sum([int(a) * int(b) for a, b in operations])


def part_one(path: Path) -> int:
    text = parse_file(path)
    return execute_mul(text)


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    text = parse_file(path)
    valid_sequences = split_by_do_or_dont(text)
    return sum(map(execute_mul, valid_sequences))


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
