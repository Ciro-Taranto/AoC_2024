from __future__ import annotations
from pathlib import Path
from itertools import product
from tqdm import tqdm
from collections import deque

from aoc_utils import timing

Point = tuple[int, int]


class HikingMap:
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, lines: list[list[int]]):
        self.lines = lines
        self.max_x = len(lines[0])
        self.max_y = len(lines)
        self.reachable_ends: dict[Point, set[Point]] = {}
        self.zeros = {
            (i, j)
            for i, j in product(range(self.max_y), range(self.max_x))
            if self[(i, j)] == 0
        }

    def __getitem__(self, point: Point) -> int:
        return self.lines[point[0]][point[1]]

    @classmethod
    def from_input(cls, path: Path) -> HikingMap:
        with path.open("r") as fin:
            text = fin.read()
        lines = []
        for line in text.split("\n"):
            lines.append(list(map(int, line.strip())))
        return HikingMap(lines)

    def get_next(self, point: Point, max_height_diff: int = 1) -> tuple[Point, int]:
        np = []
        height = self[point]
        for direction in self.directions:
            p = self.add_direction(point, direction)
            if (0 <= p[0] < self.max_y) and (0 <= p[1] < self.max_x):
                next_height = self[p]
                if 0 < next_height - height <= max_height_diff:
                    np.append((p, next_height))
        return np

    @staticmethod
    def add_direction(point: Point, direction: tuple[int, int]):
        return point[0] + direction[0], point[1] + direction[1]

    def explore(self) -> dict[Point, list[Point]]:
        # For the moment I will live without caching
        trails = {}
        for start in tqdm(self.zeros):
            trails[start] = self.explore_one(start)
        return trails

    def explore_one(self, start: Point) -> list[Point]:
        # I will use BFS instead of recursion, since we have to explore
        # all the space anyhow
        # Note: there is no way to go back nor to make loops, this might change next!
        reachable_ends = []
        queue = deque([(start, self[start])])
        while queue:
            lp, _ = queue.popleft()
            for np, nh in self.get_next(lp):
                if nh == 9:
                    reachable_ends.append(np)
                else:
                    queue.append((np, nh))
        return reachable_ends


def parse_file(path: Path) -> HikingMap:
    return HikingMap.from_input(path)


def part_one(path: Path) -> int:
    hiking_map = parse_file(path)
    trails = hiking_map.explore()
    return sum(len(set(v)) for v in trails.values())


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    hiking_map = parse_file(path)
    trails = hiking_map.explore()
    return sum(len(v) for v in trails.values())


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
