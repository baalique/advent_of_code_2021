from dataclasses import dataclass
from functools import reduce
from typing import List, Set


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def parse_data(data: str) -> List[List[int]]:
    return list(map(lambda r: list(map(int, r)), data.split("\n")))


def get_lowest_points(area: List[List[int]]) -> List[Point]:
    return list(filter(lambda p: is_lowest_point(area, p), get_all_points(area)))


def get_lowest_points_values(area: List[List[int]], points: List[Point]) -> List[int]:
    return list(map(lambda p: area[p.x][p.y], points))


def get_all_points(area: List[List[int]]) -> List[Point]:
    return [Point(x, y) for x in range(len(area)) for y in range(len(area[0]))]


def is_lowest_point(area: List[List[int]], point: Point) -> bool:
    return all(map(lambda p: area[point.x][point.y] < p,
                   map(lambda p: area[p.x][p.y], get_adjacent_points(area, point))))


def is_point_in_area(area: List[List[int]], point: Point) -> bool:
    return (point.x >= 0) and (point.y >= 0) and (point.x < len(area)) and (point.y < len(area[0]))


def get_adjacent_points(area: List[List[int]], point: Point) -> List[Point]:
    possible_points = [
        Point(point.x, point.y - 1), Point(point.x, point.y + 1),
        Point(point.x - 1, point.y), Point(point.x + 1, point.y)
    ]
    return list(filter(lambda p: is_point_in_area(area, p), possible_points))


def get_all_basins(area: List[List[int]], lowest_points: List[Point]) -> List[Set[Point]]:
    return list(map(lambda p: get_basin(area, p, {p}), lowest_points))


def get_basin(area: List[List[int]], point: Point, visited: Set[Point]) -> Set[Point]:
    adjacent_points = get_adjacent_points(area, point)
    increasing_points = set(
        filter(lambda p: p not in visited and area[point.x][point.y] < area[p.x][p.y] < 9, adjacent_points))
    return reduce(lambda acc, x: acc.union(x),
                  map(lambda p: get_basin(area, p, visited.union({p})), increasing_points),
                  set()) \
        if increasing_points else visited.union({point})


def solve_part_1(data: str) -> int:
    area = parse_data(data)
    lowest_points = get_lowest_points(area)
    return sum(get_lowest_points_values(area, lowest_points)) + len(lowest_points)


def solve_part_2(data: str) -> int:
    area = parse_data(data)
    lowest_points = get_lowest_points(area)
    all_basins_areas = sorted(map(len, (get_all_basins(area, lowest_points))))
    return reduce(lambda acc, x: acc * x, all_basins_areas[-3:])


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
