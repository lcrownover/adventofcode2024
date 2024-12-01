#!/usr/bin/env python3

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

list1 = [int(line.split()[0]) for line in lines]
list2 = [int(line.split()[1]) for line in lines]

map = {}
for i in list2:
    if i not in map:
        map[i] = 0
    map[i] += 1

acc = 0
for i in list1:
    if i in map:
        acc += map[i] * i

print(acc)
