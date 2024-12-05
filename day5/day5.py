from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from functools import cached_property
from typing import Optional

from aoc_utils import timing

Rule = dict[int, set[int]]
PrecedingPageRules = dict[int, set[int]]


class Manual:
    # If I was fully awake this would inherit from list
    def __init__(self, pages: list[int]):
        self.pages = pages

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, item: int) -> int:
        return self.pages[item]

    @classmethod
    def from_line(cls, line: str) -> Manual:
        return Manual(list(map(int, line.strip().split(","))))

    @cached_property
    def middle_page(self):
        return self.pages[len(self) // 2]

    def respects_rules(self, rules: PrecedingPageRules) -> bool:
        for i, val in enumerate(self):
            pages_before = rules.get(val, {})
            if set(pages_before).intersection(self[i:]):
                return False
        return True

    def violates_rule(self, rules: PrecedingPageRules) -> Optional[tuple[int, int]]:
        """
        Returns:
        the index of the value that should be moved and the index after which it should be inserted
        """
        for i, val in enumerate(self):
            pages_before = rules.get(val, {})
            for j in range(i + 1, len(self)):
                if self[j] in pages_before:
                    return i, j
        return None

    def fix(self, rules: PrecedingPageRules) -> Manual:
        """
        Note: before relying on the swapping of the offending pairs, I was using a
        different technique, which inserted the page that should have been before
        just before the page that was misplaced.
        This yielded valid manuals, that did not violate any rule, but that gave the wrong result!
        Also, this technique worked well on the example.
        """
        new_manual = self
        # Efficiency consideration, this scales O(N^2)
        # Maybe it could be made efficient by not checking anymore
        # before the indexes that were checked already
        # However, I am not sure it requires some assumptions on the rules to be consistent
        while (swap_tuple := new_manual.violates_rule(rules)) is not None:
            a, b = swap_tuple
            new_list = new_manual.pages.copy()
            new_list[a], new_list[b] = new_list[b], new_list[a]
            new_manual = Manual(new_list)
        return new_manual


def parse_file(path: Path) -> tuple[PrecedingPageRules, list[Manual]]:
    rules = defaultdict(set)
    manuals = list()
    with path.open("r") as fin:
        rules_lines, manual_lines = fin.read().split("\n\n")
    for rule_line in rules_lines.strip().split("\n"):
        before_page, after_page = rule_line.split("|")
        rules[int(after_page)].add(int(before_page))
    for line in manual_lines.strip().split("\n"):
        manuals.append(Manual.from_line(line))
    return rules, manuals


def part_one(path: Path) -> int:
    rules, manuals = parse_file(path)
    return sum(manual.middle_page for manual in manuals if manual.respects_rules(rules))


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def part_two(path: Path) -> int:
    rules, manuals = parse_file(path)
    incorrectly_ordered = [
        manual for manual in manuals if not manual.respects_rules(rules)
    ]
    fixed = [manual.fix(rules) for manual in incorrectly_ordered]
    return sum(manual.middle_page for manual in fixed)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
