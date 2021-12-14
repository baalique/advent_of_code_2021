from enum import Enum
from functools import reduce
from typing import List, Optional


class WrongCharacter(Enum):
    Parentheses = 3
    Square = 57
    Curly = 1197
    Angle = 25137


class MissingCharacter(Enum):
    Parentheses = 1
    Square = 2
    Curly = 3
    Angle = 4


def parse_data(data: str) -> List[List[str]]:
    return list(map(list, data.split("\n")))


def check_row(row: List[str], stack: List[str]) -> None | WrongCharacter | List[MissingCharacter]:
    match row, stack:
        case [hd, *tl], _ if hd in "([{<":
            return check_row(tl, [hd] + stack)
        case [hd, *tl], [shd, *stl] if are_brackets_match(shd, hd):
            return check_row(tl, stl)
        case [hd, *_], [shd, *_] if not are_brackets_match(shd, hd):
            return get_wrong_character(hd)
        case [], _:
            return list(map(get_missing_character, stack))
        case _:
            return


def are_brackets_match(b1: str, b2: str) -> bool:
    return b1 + b2 in ["()", "[]", "{}", "<>"]


def get_wrong_character(c: str) -> Optional[WrongCharacter]:
    return {
        ")": WrongCharacter.Parentheses,
        "]": WrongCharacter.Square,
        "}": WrongCharacter.Curly,
        ">": WrongCharacter.Angle,
    }.get(c)


def get_missing_character(c: str) -> Optional[MissingCharacter]:
    return {
        "(": MissingCharacter.Parentheses,
        "[": MissingCharacter.Square,
        "{": MissingCharacter.Curly,
        "<": MissingCharacter.Angle,
    }.get(c)


def get_autocomplete_score(chrs: List[MissingCharacter]) -> int:
    return reduce(lambda acc, x: acc * 5 + x.value, chrs, 0)


def get_middle_value_of_list(xs: List[int]) -> int:
    return sorted(xs)[len(xs) // 2]


def get_all_wrong_characters(rows: List[List[str]]) -> List[WrongCharacter]:
    return list(filter(lambda c: isinstance(c, WrongCharacter), map(lambda r: check_row(r, []), rows)))


def get_all_missing_characters(rows: List[List[str]]) -> List[List[MissingCharacter]]:
    return list(filter(lambda c: not isinstance(c, WrongCharacter), map(lambda r: check_row(r, []), rows)))


def solve_part_1(data: str) -> int:
    wrong = get_all_wrong_characters(parse_data(data))
    return sum(map(lambda c: c.value, wrong))


def solve_part_2(data: str) -> int:
    missing = get_all_missing_characters(parse_data(data))
    return get_middle_value_of_list(list(map(get_autocomplete_score, missing)))


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
