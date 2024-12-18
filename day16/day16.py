from pathlib import Path
from typing import TypeAlias, Sequence
from heapq import heappush, heappop
from tqdm import tqdm

from aoc_utils import timing


Vector: TypeAlias = tuple[int, int]
Point: TypeAlias = tuple[int, int]

DIRECTIONS = {
    (1, 0): [(0, 1), (0, -1)],
    (-1, 0): [(0, 1), (0, -1)],
    (0, 1): [(1, 0), (-1, 0)],
    (0, -1): [(1, 0), (-1, 0)],
}


def add(point: Point, vector: Vector) -> Point:
    return point[0] + vector[0], point[1] + vector[1]


class Maze:
    position: Point
    direction: Vector
    target: Point
    rotation_cost = 1000
    step_cost = 1

    def __init__(self, maze_text: str):
        self.obstacles = set()
        self.direction = (0, 1)
        for i, line in enumerate(lines := maze_text.strip().split("\n")):
            for j, char in enumerate(line):
                if char == "S":
                    self.position = (i, j)
                if char == "E":
                    self.target = (i, j)
                if char == "#":
                    self.obstacles.add((i, j))
        self.max_x = len(lines[0])
        self.max_y = len(lines)
        assert all((0, p) in self.obstacles for p in range(self.max_x))
        assert all((self.max_y - 1, p) in self.obstacles for p in range(self.max_x))
        assert all((p, 0) in self.obstacles for p in range(self.max_x))
        assert all((p, self.max_x - 1) in self.obstacles for p in range(self.max_x))

    def get_moves(self, point: Point, vector: Vector) -> list[int, Point, Vector]:
        moves = []
        if (np := add(point, vector)) not in self.obstacles:
            moves.append((self.step_cost, np, vector))
        for nv in DIRECTIONS[vector]:
            if (np := add(point, nv)) not in self.obstacles:
                moves.append((self.rotation_cost + self.step_cost, np, nv))
        return moves

    def explore(self) -> tuple[int, list[Point]]:
        queue = []
        heappush(queue, (0, self.position, self.direction, [self.position]))
        visited = set()
        pbar = tqdm()
        while queue:
            cost, position, direction, path = heappop(queue)
            pbar.update(1)
            pbar.set_postfix({"ql": len(queue)})
            if position == self.target:
                return cost, path
            for mc, mp, md in self.get_moves(position, direction):
                if (mp, md) not in visited:
                    visited.add((mp, md))
                    state = (cost + mc, mp, md, list(path) + [mp])
                    heappush(queue, state)
        raise ValueError

    def explore_p2(self) -> tuple[int, list[list[Point]]]:
        """
        The problem is probably endless loops
        """
        best_score = 10**9
        all_best_paths = []
        visited = {}
        queue = []
        heappush(queue, (0, self.position, self.direction, [self.position]))
        # pbar = tqdm()
        while queue:
            cost, position, direction, path = heappop(queue)
            visited[position] = cost
            # pbar.update(1)
            # pbar.set_postfix(
            #     {"ql": len(queue), "bs": best_score, "ns": len(all_best_paths)}
            # )
            if position == self.target:
                if cost <= best_score:
                    best_score = cost
                    all_best_paths.append(path)
                else:
                    return best_score, all_best_paths
            for mc, mp, md in self.get_moves(position, direction):
                if cost + mc <= visited.get(mp, 10**9) + self.rotation_cost:
                    state = (cost + mc, mp, md, list(path) + [mp])
                    heappush(queue, state)
        return best_score, all_best_paths

    def pprint(self, path: Sequence[Point]) -> str:
        path = set(path)
        lines = list()
        for i in range(self.max_y):
            line = []
            for j in range(self.max_x):
                if (i, j) in self.obstacles:
                    line.append("#")
                elif (i, j) in path:
                    line.append("@")
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)


def parse_file(path: Path) -> Maze:
    with path.open("r") as fin:
        return Maze(fin.read().strip())


def part_one(path: Path) -> int:
    maze = parse_file(path)
    cost, path = maze.explore()
    maze.pprint(path)
    return cost


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    maze = parse_file(path)
    _, paths = maze.explore_p2()
    seats = set()
    for path in paths:
        seats = seats.union(path)
    print(seats)
    print(maze.pprint(seats))
    return len(seats)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
