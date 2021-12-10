from typing import List, Callable


def parse_data(data: str) -> List[int]:
    return list(map(int, data.split(",")))


def match_positions_to_linear(positions: List[int], to: int) -> int:
    return sum(map(lambda pos: abs(pos - to), positions))


def match_positions_to_progressive(positions: List[int], to: int) -> int:
    return sum(map(lambda pos: (lambda n: int(n * (n + 1) / 2))(abs(pos - to)), positions))


def get_cheapest_movement(positions: List[int], movement_rule: Callable[[List[int], int], int]) -> int:
    return min(map(lambda pos: movement_rule(positions, pos), range(min(positions), max(positions) + 1)))


def solve_part_1(data: str) -> int:
    return get_cheapest_movement(parse_data(data), movement_rule=match_positions_to_linear)


def solve_part_2(data: str) -> int:
    return get_cheapest_movement(parse_data(data), movement_rule=match_positions_to_progressive)


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
