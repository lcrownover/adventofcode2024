#!/usr/bin/env python3

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

list1 = sorted([int(line.split()[0]) for line in lines])
list2 = sorted([int(line.split()[1]) for line in lines])

acc = 0
for i in range(len(list1)):
    acc += abs(list1[i] - list2[i])

print(acc)
