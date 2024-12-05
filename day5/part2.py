#!/usr/bin/env python3

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def score(update: list[str]) -> int:
    return int(update[len(update) // 2])


def order(rules: list[list[str]], failed_update: list[str]) -> list[str]:
    """
    This works by converting the list of rules into a dictionary where the key
    is the number on the left-hand side of each rule and the value is the
    occurrence of that number in that place.
    With the rules ordered the way, we can assume the numbers should be ordered
    by their occurrence value.
    """
    filtered_rules = [
        rule
        for rule in rules
        if (rule[0] in failed_update and rule[1] in failed_update)
    ]
    map = {}
    for rule in filtered_rules:
        if rule[0] not in map:
            map[rule[0]] = 0
        map[rule[0]] += 1
    return [
        key
        for key in dict(
            sorted(map.items(), key=lambda item: item[1], reverse=True)
        ).keys()
    ]


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

failed_lists = []
for update in lists:
    checked = []
    ok = True
    for pagenum in update:
        if not ok:
            break
        for rule in rules:
            if pagenum == rule[1]:
                if rule[0] in update and rule[0] not in checked:
                    ok = False
                    break
        checked.append(pagenum)
    if not ok:
        failed_lists.append(update)

out = 0

for fl in failed_lists:
    out += score(order(rules, fl))

print(out)
