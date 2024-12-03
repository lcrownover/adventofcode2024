#!/usr/bin/env python3

import re

with open("input.txt") as f:
    s = " ".join([line.strip() for line in f.readlines() if line.strip()])

acc = 0
for match in re.findall(r"mul\(\d+,\d+\)", s):
    n1, n2 = re.findall(r"\d+", match)
    acc += int(n1) * int(n2)

print(acc)
