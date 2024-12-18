from pathlib import Path
from typing import TypeAlias, Optional
from typing_extensions import Self
from tqdm import tqdm

from aoc_utils import timing

Point: TypeAlias = tuple[int, int]
Vector: TypeAlias = tuple[int, int]

DIRECTIONS = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def add(point: Point, vector: Vector) -> Point:
    return point[0] + vector[0], point[1] + vector[1]


class RobotMap:
    def __init__(
        self,
        boxes: set[Point],
        obstacles: set[Point],
        robot: Point,
        max_x: int,
        max_y: int,
        moves: list[Vector],
    ):
        self.boxes = boxes
        self.obstacles = obstacles
        self.robot = robot
        self.max_x = max_x
        self.max_y = max_y
        self.moves = moves

    @classmethod
    def from_file(cls, path: Path) -> Self:
        with path.open("r") as fin:
            map_text, moves_text = fin.read().strip().split("\n\n")
        robot = None
        boxes = set()
        obstacles = set()
        for y, line in enumerate(lines := map_text.strip().split("\n")[1:-1]):
            for x, char in enumerate(line[1:-1]):
                if char == "@":
                    robot = (y, x)
                if char == "O":
                    boxes.add((y, x))
                if char == "#":
                    obstacles.add((y, x))
        if robot is None:
            raise ValueError
        max_y = len(lines)
        max_x = len(lines[0]) - 2
        moves = list()
        for char in moves_text:
            if char != "\n":
                moves.append(DIRECTIONS[char])
        return cls(boxes, obstacles, robot, max_x, max_y, moves)

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point[0] < self.max_y and 0 <= point[1] < self.max_x

    def valid(self, point: Point) -> bool:
        return self.in_bounds(point) and point not in self.obstacles

    def move_one(self, move: Vector) -> None:
        next_robot = add(self.robot, move)
        if not self.valid(next_robot):
            return None
        if next_robot in self.boxes:
            advanced_box = next_robot
            while advanced_box in self.boxes:
                advanced_box = add(advanced_box, move)
            if not self.valid(advanced_box):
                return None
            self.boxes.remove(next_robot)
            self.boxes.add(advanced_box)
        self.robot = next_robot

    def move_all(self) -> None:
        for move in tqdm(self.moves):
            self.move_one(move)

    def __str__(self) -> str:
        lines = ["#" * (self.max_x + 2)]
        for y in range(self.max_y):
            line = ["#"]
            for x in range(self.max_x):
                if (y, x) in self.boxes:
                    line.append("O")
                elif (y, x) == self.robot:
                    line.append("@")
                elif (y, x) in self.obstacles:
                    line.append("#")
                else:
                    line.append(".")
            line.append("#")
            lines.append("".join(line))
        lines.append("#" * (self.max_x + 2))
        return "\n".join(lines)


class WideRobotMap:
    def __init__(
        self,
        boxes: set[Point],
        obstacles: set[Point],
        robot: Point,
        max_x: int,
        max_y: int,
        moves: list[Vector],
    ):
        """
        The convention is that we store
        only the location of the left edge of the box
        and of the obstacles
        """
        self.boxes = boxes
        self.obstacles = obstacles
        self.robot = robot
        self.max_x = max_x
        self.max_y = max_y
        self.moves = moves

    @classmethod
    def from_file(cls, path: Path) -> Self:
        with path.open("r") as fin:
            map_text, moves_text = fin.read().strip().split("\n\n")
        robot = None
        boxes = set()
        obstacles = set()
        for y, line in enumerate(lines := map_text.strip().split("\n")[1:-1]):
            for x, char in enumerate(line[1:-1]):
                if char == "@":
                    robot = (y, 2 * x)
                if char == "O":
                    boxes.add((y, 2 * x))
                if char == "#":
                    obstacles.add((y, 2 * x))
        if robot is None:
            raise ValueError
        max_y = len(lines)
        max_x = 2 * (len(lines[0]) - 2)
        moves = list()
        for char in moves_text:
            if char != "\n":
                moves.append(DIRECTIONS[char])
        return cls(boxes, obstacles, robot, max_x, max_y, moves)

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point[0] < self.max_y and 0 <= point[1] < self.max_x

    def robot_intercepts_item(self, point: Point, items: set[Point]) -> Optional[Point]:
        if point in items:
            return point
        if (pm := (point[0], point[1] - 1)) in items:
            return pm
        return None

    def item_intercepts_item(self, item: Point, items: set[Point]) -> set[Point]:
        intercepted = set()
        for i in range(-1, 2):
            if (ps := (item[0], item[1] + i)) in items:
                intercepted.add(ps)
        return intercepted

    def is_robot_valid(self, point: Point) -> bool:
        return self.in_bounds(point) and (
            self.robot_intercepts_item(point, self.obstacles) is None
        )

    def is_item_in_bounds(self, item: Point) -> bool:
        return 0 <= item[0] < self.max_y and 0 <= item[1] and item[1] + 1 < self.max_x

    def is_item_valid(self, item: Point) -> bool:
        return self.is_item_in_bounds(item) and not self.item_intercepts_item(
            item, self.obstacles
        )

    def move_boxes(
        self, next_robot: Point, move: Vector
    ) -> tuple[bool, dict[Point, Point]]:
        updates = {}
        if (
            intercepted_box := self.robot_intercepts_item(next_robot, self.boxes)
        ) is not None:
            intercepted_boxes = {intercepted_box}
        else:
            intercepted_boxes = {}
        while intercepted_boxes:
            box = intercepted_boxes.pop()
            next_box_position = add(box, move)
            if not self.is_item_valid(next_box_position):
                return False, {}
            updates[box] = next_box_position
            for box_to_displace in self.item_intercepts_item(
                next_box_position, self.boxes
            ).difference({box}):
                intercepted_boxes.add(box_to_displace)
        return True, updates

    def move_one(self, move: Vector) -> None:
        next_robot = add(self.robot, move)
        if not self.is_robot_valid(next_robot):
            return None
        can_move, updates = self.move_boxes(next_robot, move)
        if can_move:
            self.robot = next_robot
            self.boxes = self.boxes.difference(updates.keys())
            self.boxes = self.boxes.union(updates.values())
        return None

    def move_all(self) -> None:
        for move in tqdm(self.moves):
            self.move_one(move)

    def __str__(self) -> str:
        lines = ["#" * (self.max_x + 4)]
        for y in range(self.max_y):
            line = ["##"]
            for x in range(self.max_x):
                if (y, x) in self.boxes:
                    line.append("[")
                elif (y, x - 1) in self.boxes:
                    line.append("]")
                elif (y, x) == self.robot:
                    line.append("@")
                elif (y, x) in self.obstacles:
                    line.append("#")
                elif (y, x - 1) in self.obstacles:
                    line.append("#")
                else:
                    line.append(".")
            line.append("##")
            lines.append("".join(line))
        lines.append("#" * (self.max_x + 4))
        return "\n".join(lines)


def parse_file(path: Path) -> RobotMap:
    return RobotMap.from_file(path)


def part_one(path: Path) -> int:
    robot_map = parse_file(path)
    robot_map.move_all()
    print(robot_map)
    return sum(100 * (y + 1) + (x + 1) for y, x in robot_map.boxes)


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    wide_robot_map = WideRobotMap.from_file(path)
    wide_robot_map.move_all()
    # print(wide_robot_map)
    return sum(100 * (y + 1) + x + 2 for y, x in wide_robot_map.boxes)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
