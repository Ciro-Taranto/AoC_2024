from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict
import re


operations = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}


@dataclass(frozen=True)
class Node:
    operation: str
    left: str
    right: str


def parse(path: Path) -> Wires:
    with path.open("r") as fin:
        txt = fin.read()
    values_txt, wiring_txt = txt.split("\n\n")
    values = re.findall("(.+): ([0-1])", values_txt)
    values = {k: int(v) for k, v in values}
    assert len(values) == len(values_txt.split("\n"))
    wiring = (
        re.findall("(.+) (OR) (.+) -> (.+)", wiring_txt)
        + re.findall("(.+) (XOR) (.+) -> (.+)", wiring_txt)
        + re.findall("(.+) (AND) (.+) -> (.+)", wiring_txt)
    )
    return Wires(values, wiring)


class Wires:
    def __init__(self, values: dict[str, int], wiring: list[tuple[str, str, str, str]]):
        self.values = values
        self.connections: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
        self.parents = dict()
        for l, op, r, t in wiring:
            self.connections[l].append((op, r, t))
            self.connections[r].append((op, l, t))
            self.parents[t] = ((l, r), op)
        self.connections = {k: sorted(v) for k, v in self.connections.items()}

    def do(self) -> dict[str, int]:
        new_values = self.values
        while new_values := self.accumulate(new_values):
            self.values |= new_values
        return self.values

    def accumulate(self, values: dict[str, int]) -> dict[str, int]:
        new_values = {}
        for k, v in values.items():
            if k not in self.connections:
                continue
            for op, other, t in self.connections[k]:
                if (other in self.values) or (other in values) and t not in self.values:
                    new_values[t] = operations[op](
                        v, self.values.get(other, 0) or values.get(other, 0)
                    )
        return new_values

    def get_subtree(self, node: str) -> dict[str, tuple[dict, dict]]:
        if node not in self.parents:
            return node
        (l, r), op = self.parents[node]
        return {op: [self.get_subtree(l), self.get_subtree(r)]}

    def navigate(self, connections: dict[str, list[tuple[str, str, str]]]) -> ...:
        xs = self.xs
        ys = self.ys
        (_, _, and_t), (_, _, _) = connections[xs[0]]
        acc = and_t
        # The accumulation should go with the least significant digit of the current.
        # In formula:
        #   z_i = (x_i XOR y_i) XOR rep
        # The report is:
        # (x_i AND y_i) OR [(x_1 XOR y_1) AND rep]
        possible_issues = []
        is_problematic = False
        for x in xs[1:]:
            prev_acc = acc  # for debugging only
            prev_problematic = is_problematic  # acc might not be correct
            is_problematic = False
            (_, _, and_t), (_, _, xor_t) = connections[x]
            connections_xor = connections.get(xor_t, [])
            connections_and = connections.get(and_t, [])

            if len(connections_xor) != 2:
                is_problematic = True
            else:
                (_, r1, tr1), (_, r2, ez) = connections_xor
                is_problematic = is_problematic or (
                    (ez != x.replace("x", "z")) or (r1 != r2) or (r1 != acc)
                )
            if len(connections_and) != 1:
                is_problematic = True
            else:
                exp_or, ex_tr1, acc = connections_and[0]
                if (exp_or != "OR") or (ex_tr1 != tr1):
                    is_problematic = True

            if is_problematic:
                print(f"Possible issue with: {x}")
                possible_issues.append((x, and_t, xor_t))
        return

    def check_basic_ops(self) -> list[tuple[str, str]]:
        violations = []
        for x, y in zip(self.xs, self.ys):
            (first_op, y_1, and_t), (second_op, y_2, xor_t) = self.connections[x]
            if not (y_1 == y and y_2 == y) or not (
                first_op == "AND" and second_op == "XOR"
            ):
                violations.append((x, y))
        return violations

    @property
    def xs(self) -> list[str]:
        return sorted([x for x in self.connections if x.startswith("x")])

    @property
    def ys(self) -> list[str]:
        return sorted([y for y in self.connections if y.startswith("y")])


if __name__ == "__main__":
    path = Path(__file__).parent / "input.txt"
    wires = parse(path)
    wires.do()
    z = [v for k, v in dict(sorted(wires.values.items())).items() if k.startswith("z")]
    print(sum(2**i * v for i, v in enumerate(z)))
    wires.navigate(wires.connections)
    print(",".join(sorted("thm,z08,wss,wrm,z22,hwq,gbs,z29".split(","))))
