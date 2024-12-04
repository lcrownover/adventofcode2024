#!/usr/bin/env python3

with open("input.txt") as f:
    board = [list(line.strip()) for line in f.readlines() if line.strip()]


def safe_get_coord_str(board: list[list[str]], xy: tuple[int, int]) -> str | None:
    try:
        return board[xy[1]][xy[0]]
    except IndexError:
        return None


def find_adjacent_directional_letter_coords(
    board: list[list[str]], xy: tuple[int, int], direction: str, target_letter: str
) -> tuple[int, int] | None:
    match direction:
        case "ul":
            coord = (xy[0] - 1, xy[1] - 1)
        case "uu":
            coord = (xy[0], xy[1] - 1)
        case "ur":
            coord = (xy[0] + 1, xy[1] - 1)
        case "dl":
            coord = (xy[0] - 1, xy[1] + 1)
        case "dd":
            coord = (xy[0], xy[1] + 1)
        case "dr":
            coord = (xy[0] + 1, xy[1] + 1)
        case "ll":
            coord = (xy[0] - 1, xy[1])
        case "rr":
            coord = (xy[0] + 1, xy[1])
        case _:
            return None

    if coord[0] < 0 or coord[1] < 0:
        return None
    # print(
    #     f"  Searching for letter '{target_letter}' in adjacent xy({coord[0]=},{coord[1]=}) direction {direction}"
    # )
    letter = safe_get_coord_str(board, coord)
    if letter == target_letter:
        # print(
        #     f"  Found adjacent letter '{target_letter}' at ({coord[0]},{coord[1]}) anchored to ({xy[0]},{xy[1]})"
        # )
        return coord
    return None


def find_xmass(board: list[list[str]], xy: tuple[int, int]) -> int:
    letters = ["M", "A", "S"]
    found = 0

    def find(xy, direction, letter_idx):
        # print(
        #     f"Searching for letter {letters[letter_idx]} anchored to ({xy[0]},{xy[1]}) direction: {direction}"
        # )
        nonlocal found
        # search adjacent to xy in direction for the letters[letter_idx]
        adjacent_letter_xy = find_adjacent_directional_letter_coords(
            board, xy, direction, letters[letter_idx]
        )
        if not adjacent_letter_xy:
            return
        if letters[letter_idx] == "S":
            found += 1
            return
        # print(
        #     f"Found letter: {letters[letter_idx]} at ({adjacent_letter_xy[0]},{adjacent_letter_xy[1]})"
        # )
        find(adjacent_letter_xy, direction, letter_idx + 1)

    for direction in ["ul", "uu", "ur", "ll", "rr", "dl", "dd", "dr"]:
        find(xy, direction, 0)

    return found


count = 0
xs = 0
# print("Board:")
# [print(row) for row in board]
for y, row in enumerate(board):
    for x, col in enumerate(row):
        if safe_get_coord_str(board, (x, y)) == "X":
            # print(f"Found start of XMAS at ({x},{y})")
            count += find_xmass(board, (x, y))

print(count)
