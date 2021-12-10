from functools import reduce
from typing import List, Set, Tuple


class Board:
    def __init__(self, rows: List[List[int]]):
        self.lines = self.get_lines(rows)

    def draw_number(self, n: int):
        self.lines = list(map(lambda line: line - {n}, self.lines))

    @property
    def is_winner(self) -> bool:
        return any(map(lambda line: line == set(), self.lines))

    @property
    def score(self) -> int:
        return sum(reduce(lambda acc, x: acc.union(x), self.lines))

    @staticmethod
    def get_lines(board: List[List[int]]) -> List[Set[int]]:
        rows = list(map(set, board))
        columns = list(map(set, zip(*board)))
        return rows + columns

    def __repr__(self) -> str:
        return str(self.lines)


def parse_data(data: str) -> Tuple[List[Board], List[int]]:
    _numbers, *_boards = data.split("\n\n")
    numbers = list(map(int, _numbers.split(",")))
    boards = list(map(string_to_board, _boards))
    return boards, numbers


def string_to_board(data: str) -> Board:
    rows = list(map(lambda r: list(map(int, filter(lambda x: x, r.split(" ")))), data.split("\n")))
    return Board(rows)


def get_winner(boards: List[Board], numbers: List[int]) -> Tuple[Board, int]:
    for board in boards:
        board.draw_number(numbers[0])

    winner = list(filter(lambda b: b.is_winner, boards))
    if winner:
        return winner[0], numbers[0]
    return get_winner(boards, numbers[1:])


def get_last_winner(boards: List[Board], numbers: List[int]) -> Tuple[Board, int]:
    for board in boards:
        board.draw_number(numbers[0])

    remaining_boards = list(filter(lambda b: not b.is_winner, boards)) if len(boards) > 1 else boards

    if len(remaining_boards) == 1 and remaining_boards[0].is_winner:
        return remaining_boards[0], numbers[0]

    return get_last_winner(remaining_boards, numbers[1:])


def solve_part_1(data: str) -> int:
    winner, winning_number = get_winner(*parse_data(data))
    return winner.score * winning_number


def solve_part_2(data: str) -> int:
    winner, winning_number = get_last_winner(*parse_data(data))
    return winner.score * winning_number


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
