#!/usr/bin/env python3

with open("input.txt") as f:
    board = [list(line.strip()) for line in f.readlines() if line.strip()]


def safe_get_coord_str(board: list[list[str]], xy: tuple[int, int]) -> str | None:
    try:
        return board[xy[1]][xy[0]]
    except IndexError:
        return None


def is_valid_xmas(board: list[list[str]], xy: tuple[int, int]) -> bool:
    ul = (xy[0] - 1, xy[1] - 1)
    ur = (xy[0] + 1, xy[1] - 1)
    dl = (xy[0] - 1, xy[1] + 1)
    dr = (xy[0] + 1, xy[1] + 1)
    for d in [ul, ur, dl, dr]:
        if d[0] < 0 or d[1] < 0:
            return False
    ulc = safe_get_coord_str(board, ul)
    urc = safe_get_coord_str(board, ur)
    dlc = safe_get_coord_str(board, dl)
    drc = safe_get_coord_str(board, dr)
    if not all([ulc, urc, dlc, drc]):
        return False
    sd = sorted(
        [d if d is not None else "" for d in [ulc, urc, dlc, drc]]
    )  # satisfy LSP warning about str|None
    if sd != ["M", "M", "S", "S"]:
        return False
    if ulc == "M":
        if not (urc == "M" or dlc == "M"):
            return False
    if ulc == "S":
        if not (urc == "S" or dlc == "S"):
            return False
    return True


count = 0
xs = 0
for y, row in enumerate(board):
    for x, col in enumerate(row):
        if safe_get_coord_str(board, (x, y)) == "A":
            if is_valid_xmas(board, (x, y)):
                count += 1

print(count)
