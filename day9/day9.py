from pathlib import Path
from typing import Optional

from aoc_utils import timing


def parse_file(path: Path) -> list[int]:
    with path.open("r") as fin:
        return list(map(int, fin.read().strip()))


def expand(fs: list[int]) -> list[Optional[int]]:
    # This naive approach will probably fail me in part two...
    extended_fs = []
    for i, val in enumerate(fs):
        if i % 2 == 0:
            current_id = i // 2
        else:
            current_id = None
        extended_fs.extend([current_id] * val)
    return extended_fs


def compactify(fs: list[Optional[int]]) -> list[int]:
    compact_fs = fs.copy()
    free_spaces = [i for i, val in enumerate(fs) if val is None]
    left_cursor = 0
    for right_cursor in range(len(fs) - 1, -1, -1):
        val = fs[right_cursor]
        if val is None:
            continue
        fi = free_spaces[left_cursor]
        if fi > right_cursor:
            break
        compact_fs[fi] = val
        compact_fs[right_cursor] = None
        left_cursor += 1
        if left_cursor == len(free_spaces) - 1:
            break

    return list(filter(lambda x: x is not None, compact_fs))


def part_one(path: Path) -> int:
    fs = parse_file(path)
    extended_fs = expand(fs)
    compact_fs = compactify(extended_fs)
    print(len(compact_fs), sum(val is not None for val in extended_fs))
    return sum(i * val for i, val in enumerate(compact_fs))


with timing():
    result = part_one(Path(__file__).parent / "input.txt")
print(result)

# Part two


def find_span(arr: list[Optional[int]]) -> int:
    for i, val in enumerate(arr, start=1):
        if i == 1:
            target = val
        if val != target:
            return i - 1
    return 0


def compactify_two(fs: list[int]) -> list[Optional[int]]:
    original_fs = []
    new_fs = []
    start = 0
    id_to_index = {}
    for i, span in enumerate(fs):
        fid = i // 2 if i % 2 == 0 else None
        original_fs.append((fid, start, span))
        new_fs.append((fid, start, span))
        id_to_index[fid] = i
        start += span
    for fid, fstart, fspan in reversed(original_fs):
        if fid is None:
            continue
        for i in range(len(new_fs)):
            nfsid, nfstart, nfspan = new_fs[i]
            if nfsid is not None:
                continue
            if nfstart > fstart:
                break
            if nfspan >= fspan:
                # actually do the update
                new_fs[i] = fid, nfstart, fspan
                # We do not need to compactify!
                old_index = id_to_index[fid]
                id_to_index[fid] = i
                _, start, span = new_fs[old_index]
                new_fs[old_index] = (None, start, span)
                if nfspan > fspan:
                    new_fs.insert(i + 1, (None, nfstart + fspan, nfspan - fspan))
                    # I know this is not very nice, but I want to get over with it
                    for id, index in id_to_index.items():
                        if index > i:
                            id_to_index[id] += 1
                break
    expanded_fs = []
    for fid, _, span in new_fs:
        expanded_fs.extend([fid] * span)
    return expanded_fs


def part_two(path: Path) -> int:
    fs = parse_file(path)
    extended_fs = compactify_two(fs)
    return sum(i * val for i, val in enumerate(extended_fs) if val is not None)


with timing():
    result = part_two(Path(__file__).parent / "input.txt")
print(result)
