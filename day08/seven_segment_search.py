from dataclasses import dataclass
from functools import reduce
from typing import List, Set, NewType, FrozenSet, Dict

Digit = NewType("Digit", FrozenSet[str])


@dataclass
class Entry:
    mixed_digits: Set[Digit]
    output: List[Digit]


def parse_data(data: str) -> List[Entry]:
    return list(map(parse_row, data.split("\n")))


def parse_row(row: str) -> Entry:
    left, right = list(map(str.strip, row.split("|")))
    return Entry(
        mixed_digits=set(map(lambda s: Digit(frozenset(s)), left.split(" "))),
        output=list(map(lambda s: Digit(frozenset(s)), right.split(" ")))
    )


def restore_digits(mixed_digits: Set[Digit]) -> Dict[Digit, int]:
    _1 = list(filter(lambda d: len(d) == 2, mixed_digits))[0]
    _7 = list(filter(lambda d: len(d) == 3, mixed_digits))[0]
    _4 = list(filter(lambda d: len(d) == 4, mixed_digits))[0]
    _8 = list(filter(lambda d: len(d) == 7, mixed_digits))[0]
    _9 = list(filter(lambda d: len(_8 - d) == 1 and len(_4.intersection(d)) == 4, mixed_digits))[0]
    _2 = list(filter(lambda d: len(d) == 5 and len(_9 - d) == 2, mixed_digits))[0]
    _a = list(_7 - _1)[0]
    _e = list(_8 - _9)[0]
    _b = list(_9 - _2 - _1)[0]
    _f = list(_8 - _2 - {_b})[0]
    _c = list(_7 - {_a, _f})[0]
    _g = list(_8 - _4 - {_a, _e})[0]
    _d = list(_8 - {_a, _b, _c, _e, _f, _g})[0]
    _0 = Digit(frozenset((_a, _b, _c, _e, _f, _g)))
    _3 = Digit(frozenset((_a, _c, _d, _f, _g)))
    _5 = Digit(frozenset((_a, _b, _d, _f, _g)))
    _6 = Digit(_5.union({_e}))
    return {_0: 0, _1: 1, _2: 2, _3: 3, _4: 4, _5: 5, _6: 6, _7: 7, _8: 8, _9: 9}


def get_output(entry: Entry) -> List[int]:
    restored = restore_digits(entry.mixed_digits)
    return list(map(lambda o: restored.get(o), entry.output))


def solve_part_1(data: str) -> int:
    restored = list(map(get_output, parse_data(data)))
    return sum(sum(1 for digit in row if digit in (1, 4, 7, 8)) for row in restored)


def solve_part_2(data: str) -> int:
    restored = list(map(get_output, parse_data(data)))
    return sum(map(lambda r: int(reduce(lambda acc, x: str(acc) + str(x), r)), restored))


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
