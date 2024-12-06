#!/usr/bin/env python3

import time
import os
import copy
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

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            raise NotImplementedError
        return self.x == other.x and self.y == other.y

    def __add__(self, other: object) -> "Position":
        if not isinstance(other, Position):
            raise NotImplementedError
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> "Position":
        if not isinstance(other, Position):
            raise NotImplementedError
        return Position(self.x - other.x, self.y - other.y)

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

    def to(self, to_position: "Position") -> Direction:
        if self.x - to_position.x > 0:
            return Direction.LEFT
        if self.x - to_position.x < 0:
            return Direction.RIGHT
        if self.y - to_position.y < 0:
            return Direction.DOWN
        if self.y - to_position.y > 0:
            return Direction.UP
        raise Exception("uknown to direction")


class StepTaken:
    def __init__(self, positition: Position, direction: Direction):
        self.position = positition
        self.direction = direction

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StepTaken):
            raise NotImplementedError
        return self.position == other.position and self.direction == other.direction


class Obstacle(Enum):
    CRATE = "#"
    BOUNDARY = "-"
    NONE = "."


class Guard:
    def __init__(self, initial_pos: Position, facing: Direction):
        self.position = initial_pos
        self.facing = facing
        self._visited_spots = [initial_pos]
        self.vertices: list[Position] = []
        self.loop_positions: list[Position] = []

    def __str__(self) -> str:
        return f"Guard({self.position.x},{self.position.y},{self.facing})"

    def patrol(self, board: "Board") -> None:
        while True:
            os.system("clear")
            # whole path
            # board.print_guard_path(self)
            # just cursor
            board.print(self, show_path=False, show_loop_spots=True, show_vertices=True)
            # print(self.visited())
            time.sleep(0.2)

            print(f"Position: {self.position}")
            print(self.vertices)
            next_pos = self.position.peek(self.facing)
            if board.get_obstacle(next_pos) == Obstacle.NONE:
                for v in self.vertices[:-1]:
                    # print(f"    checking against vertex: {v}")
                    # print(f"    looking for direction: {self.facing.next()}")
                    try:
                        to_dir = next_pos.to(v)
                    except:
                        to_dir = None
                    # print(f"    to_dir = {to_dir}")
                    if board.clear_path(next_pos, v):
                        if to_dir == self.facing.next():
                            # print(f"    clear path {next_pos} -> {v}")
                            # print(f"    and direction {self.facing.next()}")
                            next_next_pos = next_pos.peek(self.facing)
                            if next_next_pos not in self.loop_positions:
                                # print(f"    previous vertices: {self.vertices}")
                                # print(
                                #     f"  Next position {next_pos}, found clear path to previous vertex: {v}"
                                # )
                                # print(f"  Adding loop position: {next_next_pos}")
                                self.loop_positions.append(next_next_pos)
            obstacle = board.get_obstacle(next_pos)
            match obstacle:
                case Obstacle.CRATE:
                    print(f"  Turning {self.facing.next()}")
                    self.vertices.append(self.position)
                    self.facing = self.facing.next()
                    next_pos = self.position
                case Obstacle.BOUNDARY:
                    # print("  Hit Boundary!")
                    break
            self.position = next_pos
            if next_pos not in self._visited_spots:
                self._visited_spots.append(next_pos)

            # input()

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

    def clear_path(self, vertex1: Position, vertex2: Position) -> bool:
        coords = []
        found_line = False
        if vertex1.x == vertex2.x:  # vertical line
            found_line = True
            y_coords = range(min(vertex1.y, vertex2.y) + 1, max(vertex1.y, vertex2.y))
            coords = [Position(vertex1.x, y) for y in y_coords]
        if vertex1.y == vertex2.y:  # horizontal line
            found_line = True
            x_coords = range(min(vertex1.x, vertex2.x) + 1, max(vertex1.x, vertex2.x))
            coords = [Position(x, vertex1.y) for x in x_coords]
        if not found_line:
            return False
        for pos in coords:
            if self.get_obstacle(pos) != Obstacle.NONE:
                return False
        # print(f"    {coords}")
        return True

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

    def print(
        self,
        guard: Guard,
        show_path: bool = False,
        show_loop_spots: bool = False,
        show_vertices: bool = False,
    ) -> None:
        copied_grid = copy.deepcopy(self.grid)
        if show_path:
            for pos in guard._visited_spots:
                copied_grid[pos.y][pos.x] = "X"
        if show_loop_spots:
            for pos in guard.loop_positions:
                copied_grid[pos.y][pos.x] = "O"
        if show_vertices:
            for pos in guard.vertices:
                if copied_grid[pos.y][pos.x] == "O":
                    copied_grid[pos.y][pos.x] = "0"
                else:
                    copied_grid[pos.y][pos.x] = "+"
        copied_board = Board(copied_grid)
        copied_board.register_guard(guard)
        print(copied_board)
        print(guard.visited())
        print(len(guard.loop_positions))


with open("input.txt") as f:
    grid = [list(line.strip()) for line in f.readlines() if line.strip()]

board = Board(grid)
guard = board.find_guard()
board.clear_guard(guard)
guard.patrol(board)

print(len(guard.loop_positions))

# board.print_guard_path(guard)
