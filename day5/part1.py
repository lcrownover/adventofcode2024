#!/usr/bin/env python3

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def score(update: list[str]) -> int:
    return int(update[len(update) // 2])


rules = []
lists = []
found_n = False
for line in lines:
    if line == "":
        found_n = True
        continue
    if not found_n:
        rules.append(line.split("|"))
    else:
        lists.append(line.split(","))

out = 0
for update in lists:
    # top level list iteration
    checked = []
    ok = True
    for pagenum in update:
        if not ok:
            break
        # go through each page number in the update
        for rule in rules:
            # check the pagenum against each rule
            # using the right side
            if pagenum == rule[1]:
                if rule[0] in update and rule[0] not in checked:
                    ok = False
                    break
        checked.append(pagenum)
    if ok:
        out += score(update)

print(out)
