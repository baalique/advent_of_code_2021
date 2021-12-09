from dataclasses import dataclass
from functools import reduce
from typing import List, Union


@dataclass(frozen=True)
class Forward:
    pass


@dataclass(frozen=True)
class Up:
    pass


@dataclass(frozen=True)
class Down:
    pass


Direction = Union[Forward, Up, Down]


@dataclass(frozen=True)
class Command:
    direction: Direction
    value: int


@dataclass(frozen=True)
class Position:
    horizontal: int
    depth: int


@dataclass(frozen=True)
class PositionWithAim:
    position: Position
    aim: int


def string_to_command(row: str) -> Command:
    direction_str, val = row.split(" ")
    match direction_str:
        case "forward":
            direction = Forward()
        case "up":
            direction = Up()
        case "down":
            direction = Down()
        case _:
            raise ValueError("Wrong command")
    return Command(direction, int(val))


def parse_data(data: str) -> List[Command]:
    return list(map(string_to_command, data.split("\n")))


def apply_command(position: Position, command: Command) -> Position:
    match command:
        case Command(Forward(), x):
            return Position(horizontal=position.horizontal + x, depth=position.depth)
        case Command(Up(), x):
            return Position(horizontal=position.horizontal, depth=position.depth - x)
        case Command(Down(), x):
            return Position(horizontal=position.horizontal, depth=position.depth + x)


def apply_command_with_aim(position: PositionWithAim, command: Command) -> PositionWithAim:
    match command:
        case Command(Forward(), x):
            return PositionWithAim(
                Position(horizontal=position.position.horizontal + x, depth=position.position.depth + position.aim * x),
                position.aim)
        case Command(Up(), x):
            return PositionWithAim(position.position, position.aim - x)
        case Command(Down(), x):
            return PositionWithAim(position.position, position.aim + x)


def get_final_position(commands: List[Command]) -> Position:
    return reduce(apply_command, commands, Position(0, 0))


def get_final_position_with_aim(commands: List[Command]) -> Position:
    return reduce(apply_command_with_aim, commands, PositionWithAim(Position(0, 0), 0)).position


def solve_part_1(data: str) -> int:
    final_position = get_final_position(parse_data(data))
    return final_position.horizontal * final_position.depth


def solve_part_2(data: str) -> int:
    final_position = get_final_position_with_aim(parse_data(data))
    return final_position.horizontal * final_position.depth


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
