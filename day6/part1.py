#!/usr/bin/env python3

import copy
import os
import time
from enum import Enum
from typing import Optional


class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

    def __str__(self) -> str:
        match self:
            case self.UP:
                return "UP"
            case self.RIGHT:
                return "RIGHT"
            case self.DOWN:
                return "DOWN"
            case self.LEFT:
                return "LEFT"
        raise Exception("invalid direction")

    def next(self) -> "Direction":
        match self:
            case self.UP:
                return self.RIGHT
            case self.RIGHT:
                return self.DOWN
            case self.DOWN:
                return self.LEFT
            case self.LEFT:
                return self.UP
        raise Exception("invalid direction")


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            raise NotImplementedError
        return self.x == other.x and self.y == other.y

    def peek(self, direction: Direction):
        match direction:
            case Direction.UP:
                return Position(self.x, self.y - 1)
            case Direction.RIGHT:
                return Position(self.x + 1, self.y)
            case Direction.DOWN:
                return Position(self.x, self.y + 1)
            case Direction.LEFT:
                return Position(self.x - 1, self.y)


class Obstacle(Enum):
    CRATE = "#"
    BOUNDARY = "-"
    NONE = "."


class Guard:
    def __init__(self, initial_pos: Position, facing: Direction):
        self.position = initial_pos
        self.facing = facing
        self._visited_spots = [initial_pos]

    def __str__(self) -> str:
        return f"Guard({self.position.x},{self.position.y},{self.facing})"

    def patrol(self, board: "Board") -> None:
        # frameskip = 1
        frame = 0
        while True:
            # if frameskip and frame % frameskip == 0:
            # if frame > 4000:
            #     os.system("clear")
                # whole path
                # board.print_guard_path(self)
                # just cursor
                # board.print(self)
                # print(self.visited())
                # time.sleep(0.2)
            frame += 1
            # print(f"Position: {self.position}")
            next_pos = self.position.peek(self.facing)
            obstacle = board.get_obstacle(next_pos)
            match obstacle:
                case Obstacle.CRATE:
                    # print(f"  Turning {self.facing.next()}")
                    self.facing = self.facing.next()
                    next_pos = self.position.peek(self.facing)
                case Obstacle.BOUNDARY:
                    # print(f"Position: {self.position}")
                    # print("  Hit Boundary!")
                    break
            self.position = next_pos
            if next_pos not in self._visited_spots:
                self._visited_spots.append(next_pos)

    def visited(self) -> int:
        return len(self._visited_spots)


class Board:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid

    def width(self) -> int:
        return len(self.grid[0])

    def height(self) -> int:
        return len(self.grid)

    def __str__(self) -> str:
        return "\n".join(["".join(line) for line in self.grid])

    def _print_grid(self, grid: list[list[str]]) -> None:
        print("\n".join(["".join(line) for line in grid]))

    def _get_position_str(self, position: Position) -> str | None:
        try:
            c = self.grid[position.y][position.x]
        except IndexError:
            return None
        if position.y < 0 or position.x < 0:
            return None
        return c

    def get_obstacle(self, position: Position) -> Obstacle:
        match self._get_position_str(position):
            case "#":
                return Obstacle.CRATE
            case None:
                return Obstacle.BOUNDARY
            case ".":
                return Obstacle.NONE
            case _:
                print(self._get_position_str(position))
        raise Exception(f"unknown obstacle at pos:{position}")

    def find_guard(self) -> Guard:
        for y, col in enumerate(self.grid):
            for x, c in enumerate(col):
                match c:
                    case "^":
                        return Guard(Position(x, y), facing=Direction.UP)
                    case ">":
                        return Guard(Position(x, y), facing=Direction.RIGHT)
                    case "v":
                        return Guard(Position(x, y), facing=Direction.DOWN)
                    case "<":
                        return Guard(Position(x, y), facing=Direction.LEFT)
                    case _:
                        continue
        raise Exception("Unable to find guard")

    def clear_guard(self, guard: Optional[Guard]) -> None:
        if guard:
            self.grid[guard.position.y][guard.position.x] = "."
            return
        for y, col in enumerate(self.grid):
            for x, c in enumerate(col):
                if c in [
                    Direction.UP.value,
                    Direction.RIGHT.value,
                    Direction.DOWN.value,
                    Direction.LEFT.value,
                ]:
                    self.grid[y][x] = "."

    def register_guard(self, guard: Guard) -> None:
        self.clear_guard(guard)
        try:
            self.grid[guard.position.y][guard.position.x] = guard.facing.value
        except IndexError:
            # dont print the guard if its off the edge
            return None

    def print(self, guard: Guard) -> None:
        self.register_guard(guard)
        print(self)
        self.clear_guard(guard)

    def print_guard_path(self, guard: Guard) -> None:
        copied_grid = copy.deepcopy(self.grid)
        for pos in guard._visited_spots:
            copied_grid[pos.y][pos.x] = "X"
        copied_board = Board(copied_grid)
        copied_board.register_guard(guard)
        print(copied_board)
        print(guard.visited())


with open("input.txt") as f:
    grid = [list(line.strip()) for line in f.readlines() if line.strip()]

board = Board(grid)
guard = board.find_guard()
board.clear_guard(guard)
guard.patrol(board)

board.print_guard_path(guard)
