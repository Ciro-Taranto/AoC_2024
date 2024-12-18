from pathlib import Path
from heapq import heappush, heappop
from tqdm import tqdm
from typing import Optional

from aoc_utils import timing

Point = tuple[int, int]
Vector = tuple[int, int]


class MemoryMap:
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, filepath: Path, p1: bool = True):
        with filepath.open("r") as fin:
            txt = fin.read().strip()
        max_bytes = 1024 if "example" not in filepath.name else 12
        self.corrupted = set()
        lines = txt.split("\n")
        for line in lines[:max_bytes]:
            x, y = line.strip().split(",")
            self.corrupted.add((int(x), int(y)))
        self.more_corrupted = list()
        for line in lines[max_bytes:]:
            x, y = line.strip().split(",")
            self.more_corrupted.append((int(x), int(y)))
        if "example" in filepath.name:
            max_coord = 6
        else:
            max_coord = 70
        self.max_x = max_coord
        self.max_y = max_coord

    def astar(self, start: Point, end: Point) -> Optional[list[Point]]:
        frontier = [(self.manhattan(end, start), start, [start])]
        visited = set()
        while frontier:
            _, p, path = heappop(frontier)
            if p == end:
                return path
            for np in self.next(p):
                next_path = path + [np]
                if np not in visited:
                    heappush(
                        frontier,
                        (self.manhattan(end, np), np, next_path),
                    )
                    visited.add(np)
        return None

    def find_blocker(self, start: Point, end: Point) -> Point:
        for p in tqdm(self.more_corrupted):
            self.corrupted.add(p)
            if self.astar(start, end) is None:
                return p
        raise ValueError

    def next(self, point: Point) -> list[Point]:
        candidates = []
        for direction in self.directions:
            np = point[0] + direction[0], point[1] + direction[1]
            if (
                0 <= np[0] <= self.max_x
                and 0 <= np[1] <= self.max_y
                and np not in self.corrupted
            ):
                candidates.append(np)
        return candidates

    def manhattan(self, p1: Point, p2: Point) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def draw(self, path: list[Point]) -> None:
        lines = list()
        for y in range(self.max_y + 1):
            line = list()
            for x in range(self.max_x + 1):
                if (x, y) in path:
                    line.append("@")
                elif (x, y) in self.corrupted:
                    line.append("#")
                else:
                    line.append(".")
            lines.append("".join(line))
        print("\n".join(lines))


def part_one(path: Path) -> int:
    memory_map = MemoryMap(path)
    path = memory_map.astar((0, 0), (memory_map.max_x, memory_map.max_y))
    return len(path) - 1


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> Point:
    memory_map = MemoryMap(path)
    blocker = memory_map.find_blocker((0, 0), (memory_map.max_x, memory_map.max_y))
    return blocker


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
