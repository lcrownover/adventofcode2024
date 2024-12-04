#!/usr/bin/env python3

# I thought that it was asking that you would need to check if XMAS appeared in any
# form, including nonlinear, such as this being a valid XMAS:
#
# SX
# AM
#
# But that wasn't the case, I just had to look at a line, which was much easier.

with open("test_input.txt") as f:
    board = [list(line.strip()) for line in f.readlines() if line.strip()]


def safe_get_coord_str(board: list[list[str]], xy: tuple[int, int]) -> str | None:
    try:
        return board[xy[1]][xy[0]]
    except IndexError:
        return None


def find_adjacent_letter_coords(
    board: list[list[str]], xy: tuple[int, int], target_letter: str
) -> list[tuple[int, int]]:
    ul = (xy[0] - 1, xy[1] - 1)
    uu = (xy[0], xy[1] - 1)
    ur = (xy[0] + 1, xy[1] - 1)
    dl = (xy[0] - 1, xy[1] + 1)
    dd = (xy[0], xy[1] + 1)
    dr = (xy[0] + 1, xy[1] + 1)
    ll = (xy[0] - 1, xy[1])
    rr = (xy[0] + 1, xy[1])
    found = []
    for axy in [ul, uu, ur, dl, dd, dr, ll, rr]:
        if axy[0] < 0 or axy[1] < 0:
            continue
        print(
            f"  Searching for letter '{target_letter}' in adjacent xy({axy[0]=},{axy[1]=})"
        )
        letter = safe_get_coord_str(board, axy)
        if letter == target_letter:
            print(
                f"  Found adjacent letter '{target_letter}' at ({axy[0]},{axy[1]}) anchored to ({xy[0]},{xy[1]})"
            )
            found.append(axy)
    return found


def find_xmass(board: list[list[str]], xy: tuple[int, int]) -> int:
    letters = ["M", "A", "S"]
    found = 0

    def find(xy, letter_idx):
        print(
            f"Searching for letter {letters[letter_idx]} anchored to ({xy[0]},{xy[1]})"
        )
        nonlocal found
        # search adjacent to xy for the letters[letter_idx]
        found_adjacent_letter_xys = find_adjacent_letter_coords(
            board, xy, letters[letter_idx]
        )
        if not found_adjacent_letter_xys:
            return
        if letters[letter_idx] == "S":
            # if we just searched for S's, that means we can just add the count of them to found
            found += len(found_adjacent_letter_xys)
            return
        for adjacent_letter_xy in found_adjacent_letter_xys:
            print(
                f"Found letter: {letters[letter_idx]} at ({adjacent_letter_xy[0]},{adjacent_letter_xy[1]})"
            )
            find(adjacent_letter_xy, letter_idx + 1)

    find(xy, 0)
    return found


count = 0
xs = 0
print("Board:")
[print(row) for row in board]
for y, row in enumerate(board):
    for x, col in enumerate(row):
        if safe_get_coord_str(board, (x, y)) == "X":
            print(f"Found start of XMAS at ({x},{y})")
            count += find_xmass(board, (x, y))

print(count)
