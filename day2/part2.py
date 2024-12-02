#!/usr/bin/env python3

with open("input.txt") as f:
    reports = [line.strip() for line in f.readlines() if line.strip()]


def is_increasing_safely_with_ignore(report: list[int]) -> bool:
    def is_increasing_safely(report: list[int]) -> bool:
        for i in range(len(report) - 1):
            if abs(report[i] - report[i + 1]) > 3:
                return False
            if report[i] - report[i + 1] == 0:
                return False
            if report[i] > report[i + 1]:
                return False
        return True

    if is_increasing_safely(report):
        return True
    for i in range(len(report)):
        ignored_report = report[:i] + report[i + 1 :]
        if is_increasing_safely(ignored_report):
            return True
    return False


def is_decreasing_safely_with_ignore(report: list[int]) -> bool:
    def is_decreasing_safely(report: list[int]) -> bool:
        for i in range(len(report) - 1):
            if abs(report[i] - report[i + 1]) > 3:
                return False
            if report[i] - report[i + 1] == 0:
                return False
            if report[i] < report[i + 1]:
                return False
        return True

    if is_decreasing_safely(report):
        return True
    for i in range(len(report)):
        ignored_report = report[:i] + report[i + 1 :]
        if is_decreasing_safely(ignored_report):
            return True
    return False


safe_count = 0

for report in reports:
    levels = [int(el) for el in report.split()]
    if is_increasing_safely_with_ignore(levels):
        safe_count += 1
        continue
    if is_decreasing_safely_with_ignore(levels):
        safe_count += 1
        continue

print(safe_count)
