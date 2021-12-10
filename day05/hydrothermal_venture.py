import re
from collections import Counter
from dataclasses import dataclass
from itertools import chain
from typing import List, Dict


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Line:
    p1: Point
    p2: Point


def parse_data(data: str) -> List[Line]:
    return list(map(parse_line, data.split("\n")))


def parse_line(line: str) -> Line:
    line_regex = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
    x1, y1, x2, y2 = map(int, line_regex.search(line).groups())
    return Line(Point(x1, y1), (Point(x2, y2)))


def get_points_of_line(line: Line, count_diagonals) -> List[Point]:
    match line:
        case Line(Point(x1, y1), Point(x2, y2)) if x1 == x2:
            y_min = min(y1, y2)
            y_max = max(y1, y2)
            return [Point(x1, y_min + i) for i in range(y_max - y_min + 1)]
        case Line(Point(x1, y1), Point(x2, y2)) if y1 == y2:
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            return [Point(x_min + i, y1) for i in range(x_max - x_min + 1)]
        case Line(Point(x1, y1), Point(x2, y2)) if count_diagonals and abs(x1 - x2) == abs(y1 - y2):
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            y_min = min(y1, y2)
            lines = [Point(x_min + i, y_min + i) for i in range(x_max - x_min + 1)]
            is_raising_diagonal = Point(x_min, y_min) in [Point(x1, y1), Point(x2, y2)]
            return lines if is_raising_diagonal else \
                [Point(x, y) for x, y in zip(map(lambda p: p.x, lines), reversed(list(map(lambda p: p.y, lines))))]
        case _:
            return []


def get_all_points(lines: List[Line], count_diagonals: bool = False) -> Dict[Point, int]:
    return dict(Counter(chain(*(map(lambda line: get_points_of_line(line, count_diagonals), lines)))))


def solve_part_1(data: str) -> int:
    all_points = get_all_points(parse_data(data))
    return sum(1 for v in all_points.values() if v >= 2)


def solve_part_2(data: str) -> int:
    all_points = get_all_points(parse_data(data), count_diagonals=True)
    return sum(1 for v in all_points.values() if v >= 2)


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
