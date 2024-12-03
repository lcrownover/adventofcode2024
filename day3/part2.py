#!/usr/bin/env python3


import re


def found_do(i: int, s: str) -> bool:
    if "".join(s[i : i + 4]) == "do()":
        return True
    return False


def found_dont(i: int, s: str) -> bool:
    if "".join(s[i : i + 7]) == "don't()":
        return True
    return False


def found_mul(i: int, s: str) -> bool:
    slice = "".join(s[i : i + 12])
    if re.match(r"mul\(\d+,\d+\)", slice):
        return True
    return False


def calc_mul(i: int, s: str) -> int:
    slice = "".join(s[i : i + 12])
    m = re.match(r"mul\(\d+,\d+\)", slice)
    if m:
        nums = re.findall(r"\d+", m[0])
        return int(nums[0]) * int(nums[1])
    return 0


with open("input.txt") as f:
    s = " ".join([line.strip() for line in f.readlines() if line.strip()])

acc = 0

do = True
for i, c in enumerate(s):
    if c == "d":
        if found_do(i, s):
            do = True
        if found_dont(i, s):
            do = False
    if c == "m":
        if not do:
            continue
        n = calc_mul(i, s)
        if not n:
            continue
        acc += n
print(acc)
