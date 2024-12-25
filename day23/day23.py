from collections import defaultdict
from functools import partial


def get_graph(txt: str) -> dict[str, set[str]]:
    graph = defaultdict(set)
    for a, b in map(partial(str.split, sep="-"), txt.strip().split("\n")):
        graph[a].add(b)
        graph[b].add(a)
    return graph


def find_set_of_three_connected_computers(
    graph: dict[str, set[str]]
) -> set[tuple[str, str, str]]:
    sets = set()
    for source, targets in graph.items():
        for target in targets:
            for next_target in graph[target]:
                if (next_target not in {source, target}) and next_target in targets:
                    sets.add(tuple(sorted([source, target, next_target])))
    return sets


def find_fully_connected_groups(graph: dict[str, set[str]]) -> list[set[str]]:
    all_groups = set()
    for source, targets in graph.items():
        groups = [{source, target} for target in targets]
        for group in groups:
            for next_candidate in targets.difference(group):
                if group.issubset(graph[next_candidate]):
                    group.add(next_candidate)
        groups = set(tuple(sorted(group)) for group in groups)
        all_groups = all_groups.union(groups)
    return all_groups


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        txt = f.read()
    graph = get_graph(txt)
    sets = find_set_of_three_connected_computers(graph)
    print(sum(any(elem.startswith("t") for elem in group) for group in sets))
    fully_connected = find_fully_connected_groups(graph)
    longest_group = sorted(fully_connected, key=lambda x: len(x))[-1]
    print(",".join(longest_group))
