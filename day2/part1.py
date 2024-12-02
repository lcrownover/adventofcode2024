#!/usr/bin/env python3

with open("input.txt") as f:
    reports = [line.strip() for line in f.readlines() if line.strip()]

safe_count = 0

for report in reports:
    safe = True
    dec = None
    inc = None
    levels = report.split()
    for i, level_str in enumerate(levels[1:]):
        curr_level = int(level_str)
        prev_level = int(levels[i])
        if abs(curr_level - prev_level) > 3:
            safe = False
            break
        if curr_level - prev_level == 0:
            safe = False
            break
        if curr_level > prev_level:
            inc = True
        if curr_level < prev_level:
            dec = True
        if dec and inc:
            safe = False
            break
    if safe:
        safe_count += 1

print(safe_count)
