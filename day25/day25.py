from pathlib import Path
from itertools import product

Key = tuple[int, int, int, int, int]
Lock = tuple[int, int, int, int, int]


def parse(path: Path) -> tuple[list[Lock], list[Key]]:
    with path.open("r") as fin:
        txt = fin.read()
    keys = []
    locks = []
    for elem in txt.strip().split("\n\n"):
        lines = elem.split("\n")
        if lines[0] == "#" * len(lines[0]):
            locks.append(parse_one(lines))
        else:
            keys.append(parse_one(lines[::-1]))
    return locks, keys


def parse_one(lines: list[str]) -> Lock | Key:
    lock_or_key = [0 for _ in lines[0]]
    for i, line in enumerate(lines[1:], start=1):
        for j, char in enumerate(line):
            if char == "#":
                lock_or_key[j] = i
    return tuple(lock_or_key)


def find_compatible(locks: list[Lock], keys: list[Key]) -> list[tuple[Lock, Key]]:
    fitting = list()
    for lock, key in product(locks, keys):
        if all(a + b <= 5 for a, b in zip(lock, key)):
            fitting.append((lock, key))
    return fitting


if __name__ == "__main__":
    locks, keys = parse(Path(__file__).parent / "input.txt")
    fitting = find_compatible(locks, keys)
    print(len(fitting))
