from pathlib import Path
from collections import deque, defaultdict, Counter
from math import inf
from tqdm import tqdm

from aoc_utils import timing

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

Point = tuple[int, int]


class RaceTrack:
    def __init__(
        self,
        start: Point,
        end: Point,
        obstacles: set[Point],
        max_y: int,
        max_x: int,
        max_cheat: int = 2,
    ):
        self.start = start
        self.end = end
        self.obstacles = obstacles
        self.max_x = max_x
        self.max_y = max_y
        self.frontiers_from_start = defaultdict(
            set,
            {
                0: {
                    self.start,
                }
            },
        )
        self.distance_from_target: dict[Point, int] = {}

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point[0] < self.max_y and 0 <= point[1] < self.max_x

    def get_next(self, p: Point) -> list[Point]:
        possibilities = []
        for d in DIRECTIONS:
            np = p[0] + d[0], p[1] + d[1]
            if self.in_bounds(np) and np not in self.obstacles:
                possibilities.append(np)
        return possibilities

    def from_start_to_target(self):
        visited = set()
        frontier = deque([(self.start, 0)])
        while frontier:
            p, d = frontier.popleft()
            visited.add(p)
            self.frontiers_from_start[d].add(p)
            if p == self.end:
                return
            for np in self.get_next(p):
                if np not in visited:
                    frontier.append([np, d + 1])
        raise ValueError

    def from_target_to_start(self, max_dist: int):
        frontier = deque([(self.end, 0)])
        while frontier:
            p, d = frontier.popleft()
            self.distance_from_target[p] = d
            if d >= max_dist:
                return
            for np in self.get_next(p):
                if np not in self.distance_from_target:
                    frontier.append([np, d + 1])
        raise ValueError

    def solve(self, max_cheats: int = 2) -> dict[tuple[Point, Point], int]:
        shortcuts = dict()
        self.from_start_to_target()
        max_distance = max(self.frontiers_from_start)
        self.from_target_to_start(max_distance)
        for i, ps in tqdm(self.frontiers_from_start.items()):
            for p in ps:
                for (one, two), distance in self.manhattan(p, max_cheats).items():
                    # new distance = i + max_cheats + distance from target
                    shortcut = max_distance - (
                        i + (self.distance_from_target.get(two, inf) + distance)
                    )
                    if shortcut > 0:
                        shortcuts[(one, two)] = min(
                            shortcut, shortcuts.get((one, two), inf)
                        )
        return shortcuts

    def manhattan(self, point: Point, max_cheats: int) -> dict[Point, int]:
        visitable = {}
        for i in range(-max_cheats, max_cheats + 1):
            max_x = max_cheats - abs(i)
            for j in range(-max_x, max_x + 1):
                np = point[0] + i, point[1] + j
                if self.in_bounds(np) and np not in self.obstacles:
                    visitable[(point, np)] = abs(i) + abs(j)
        return visitable


def parse_file(path: Path) -> RaceTrack:
    with path.open("r") as fin:
        txt = fin.read()
    obstacles = set()
    for y, line in enumerate(lines := txt.strip().split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                obstacles.add((y, x))
            elif char == "S":
                start = (y, x)
            elif char == "E":
                end = (y, x)
    return RaceTrack(start, end, obstacles, len(lines), len(lines[0]))


def add(point: Point, direction: Point) -> Point:
    return point[0] + direction[0], point[1] + direction[1]


def part_one(path: Path) -> int:
    race_track = parse_file(path)
    shortcuts = race_track.solve(max_cheats=2)
    return sum(val >= 100 for val in shortcuts.values())


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    race_track = parse_file(path)
    shortcuts = race_track.solve(max_cheats=20)
    return sum(val >= 100 for val in shortcuts.values())


with timing():
    result = part_two(Path(__file__).parent / "input.txt")

print(result)
