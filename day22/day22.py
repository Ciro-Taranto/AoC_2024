from pathlib import Path
from collections import deque, defaultdict


MAGIC = 16777216


def step1(n: int) -> int:
    m = n << 6
    m = n ^ m
    return m % MAGIC


def step2(n: int) -> int:
    m = n >> 5
    m = m ^ n
    return m % MAGIC


def step3(n: int) -> int:
    m = n << 11
    m = m ^ n
    return m % MAGIC


def generate(n: int) -> int:
    n = step1(n)
    n = step2(n)
    n = step3(n)
    return n


def part_one(secrets: list[int]) -> int:
    tot = 0
    for secret in secrets:
        for _ in range(2000):
            secret = generate(secret)
        tot += secret
    return tot


def part_two(secrets: list[int]) -> int:
    accumulator = defaultdict(int)
    for secret in secrets:
        seen = set()
        difference = deque(maxlen=4)
        previous = secret % 10
        for i in range(2000):
            n = generate(secret)
            value = n % 10
            difference.append(value - previous)
            if i >= 3 and (idx := tuple(difference)) not in seen:
                accumulator[idx] += value
                seen.add(idx)
            secret = n
            previous = value
    return max(accumulator.values())


with (Path(__file__).parent / "input.txt").open("r") as f:
    secrets = list(map(int, f.read().strip().split("\n")))

# print(part_one(secrets))
print(part_two(secrets))
