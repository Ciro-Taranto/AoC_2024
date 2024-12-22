from pathlib import Path
from collections import defaultdict, deque
from itertools import pairwise, product
from functools import cache
from math import inf
from itertools import product


Graph = dict[str, dict[str, str]]
Transitions = dict[tuple[str, str], list[str]]
Point: tuple[int, int]


numeric_keypad = "789\n456\n123\n.0A"
direction_keypad = ".^A\n<v>"

moves = {(-1, 0): "^", (1, 0): "v", (0, 1): ">", (0, -1): "<"}


def get_graph(input: str) -> Graph:
    pos = {}
    for i, line in enumerate(input.split("\n")):
        for j, char in enumerate(line):
            if char != ".":
                pos[(i, j)] = char
    transitions = defaultdict(dict)
    for p, button in pos.items():
        for move, symbol in moves.items():
            np = p[0] + move[0], p[1] + move[1]
            if np in pos:
                transitions[button][symbol] = pos[np]
    return transitions


def get_to_position(start: str, end: str, graph: Graph) -> list[str]:
    maxlen = inf
    frontier = deque([(start, start, "")])
    paths = []
    while frontier:
        (position, visited, pressed) = frontier.popleft()
        if position == end:
            maxlen = len(visited)
            paths.append((visited, pressed))
        if len(visited) > maxlen:
            break
        moves = graph[position]
        for move, np in moves.items():
            if np not in visited:
                frontier.append((np, visited + np, pressed + move))
    return [p for _, p in paths]


def get_transitions(
    graph: Graph,
) -> dict[tuple[str, str], list[tuple[str, str]]]:
    transitions = dict()
    for a, b in product(graph, graph):
        transitions[(a, b)] = get_to_position(a, b, graph)
    return transitions


numeric_graph = get_graph(numeric_keypad)
direction_graph = get_graph(direction_keypad)
numeric_transitions = get_transitions(numeric_graph)
directional_transitions = get_transitions(direction_graph)

# From observation, this one has less change of directions.
# Note: this works only for part one.
# For some reason the whole approach breaks at some point and
# I had to change strategy -> cannot take credit for the strategy!
directional_transitions[("<", "A")] = list(
    reversed(directional_transitions[("<", "A")])
)


def expand(
    code: str, transitions: Transitions = directional_transitions, cut: bool = False
) -> list[str]:
    generation = [""]
    for t in pairwise("A" + code):
        next_gen = []
        for i, nt in enumerate(transitions[t]):
            if i == 1 and cut:
                break
            for state in generation:
                next_gen.append(state + nt + "A")
        generation = next_gen
    return generation


def press(code: str, nesting: int = 2) -> list[str]:
    codes = expand(code, numeric_transitions)
    for _ in range(nesting):
        new_codes = []
        for code in codes:
            new_codes.extend(expand(code, directional_transitions, cut=True))
        codes = new_codes
    return codes


@cache
def press_dirpad(t: tuple[str, str], nesting: int):
    transitions = directional_transitions[t]
    if nesting == 1:
        return len(directional_transitions[t][0]) + 1
    return min(
        sum([press_dirpad(nt, nesting - 1) for nt in pairwise("A" + transition + "A")])
        for transition in transitions
    )


def press_smart(code: str, nesting: int = 2) -> int:
    codes = expand(code, numeric_transitions)
    values = []
    for code in codes:
        values.append(sum(press_dirpad(t, nesting) for t in pairwise("A" + code)))
    return min(values)


with (Path(__file__).parent / "input.txt").open("r") as fin:
    codes = fin.read().strip().split("\n")

solutions = {code: press(code, nesting=2) for code in codes}
solutions_p2 = {code: press_smart(code, nesting=25) for code in codes}

total = 0
total_p2 = 0
for code, sols in solutions.items():
    total += int(code.replace("A", "")) * min(len(sol) for sol in sols)
    total_p2 += int(code.replace("A", "")) * solutions_p2[code]
print(total)
print(total_p2)
