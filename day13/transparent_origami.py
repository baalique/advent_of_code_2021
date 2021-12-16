import re
from dataclasses import dataclass
from functools import reduce
from typing import List, Union, Tuple, Set


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class X:
    pass


class Y:
    pass


Axis = Union[X, Y]
Paper = Set[Point]


@dataclass
class Fold:
    axis: Axis
    value: int


def parse_data(data: str) -> Tuple[Paper, List[Fold]]:
    _points, _folds = data.split("\n\n")
    paper = {Point(*map(int, p.split(","))) for p in _points.split("\n")}
    folds = list(map(parse_fold, _folds.split("\n")))
    return paper, folds


def parse_fold(row: str) -> Fold:
    regex = r"fold along (x|y)=(\d+)"
    axis, value = re.search(regex, row).groups()
    return Fold(X() if axis == "x" else Y(), int(value))


def fold_paper(paper: Paper, fold: Fold) -> Paper:
    match fold.axis:
        case X():
            less = set(filter(lambda p: p.x <= fold.value, paper))
            bigger = set(filter(lambda p: p.x >= fold.value, paper))
            reflected = set(map(lambda p: Point(fold.value - (p.x - fold.value), p.y), bigger))
            return less | reflected
        case Y():
            less = set(filter(lambda p: p.y <= fold.value, paper))
            bigger = set(filter(lambda p: p.y >= fold.value, paper))
            reflected = set(map(lambda p: Point(p.x, fold.value - (p.y - fold.value)), bigger))
            return less | reflected


def print_paper(paper: Paper) -> str:
    max_x = max(map(lambda p: p.x, paper))
    max_y = max(map(lambda p: p.y, paper))
    sheet = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for point in paper:
        sheet[point.y][point.x] = "*"
    return "\n".join("".join(sheet[x][y] for y in range(len(sheet[0]))) for x in range(len(sheet)))


def solve_part_1(data: str) -> int:
    paper, folds = parse_data(data)
    return len(reduce(lambda acc, x: fold_paper(acc, x), [folds[0]], paper))


def solve_part_2(data: str) -> str:
    paper, folds = parse_data(data)
    folded_paper = reduce(lambda acc, x: fold_paper(acc, x), folds, paper)
    return print_paper(folded_paper)


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
