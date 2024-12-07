#!/usr/bin/env python3

with open("test_input.txt") as f:
    operators = [line.strip() for line in f.readlines() if line.strip()]

def create_perms(length: int) -> list[str]:
    out = []
    for i in range(length):
        



for operator in operators:
    total = operator.split(":")[0].strip()
    components = [int(c) for c in operator.split(":")[1].split()]
    print(f"Operator => {total}: {components}")
    ops = len(components) - 1
    

