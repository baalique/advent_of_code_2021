from dataclasses import dataclass
from functools import reduce
from typing import List, Callable


@dataclass(frozen=True)
class Point:
    x: int
    y: int


Grid = List[List[int]]


def parse_data(data: str) -> Grid:
    return list(map(lambda r: list(map(int, r)), data.split("\n")))


def get_cost_from_to(grid: Grid, start: Point, stop: Point) -> int:
    to_visit = {Point(x, y) for x in range(len(grid)) for y in range(len(grid[0]))} - {start}
    nodes = {start: grid[start.x][start.y]}
    cur = start

    while True:
        if cur == stop:
            return nodes.get(stop)

        for point in list(filter(lambda p: p in to_visit, get_adjacent_points(grid, cur))):
            if point not in nodes or nodes[point] > nodes[cur] + grid[point.x][point.y]:
                nodes[point] = nodes[cur] + grid[point.x][point.y]

        to_visit.discard(cur)
        nodes.pop(cur)
        min_cost = min(nodes.values())
        cur = list(filter(lambda p: nodes[p] == min_cost, nodes))[0]


def transform_grid(grid: Grid, func: Callable[[int, int, int], int], width: int, height: int) -> Grid:
    return flatten_grid([[map_grid(grid, lambda v: func(v, x, y)) for x in range(width)] for y in range(height)])


def map_grid(grid: Grid, func: Callable[[int], int]) -> Grid:
    return [[func(grid[x][y]) for y in range(len(grid[0]))] for x in range(len(grid))]


def flatten_grid(multi_grid: List[List[Grid]]) -> Grid:
    return [reduce(lambda acc, x: acc + x, [multi_grid[x][y][z] for y in range(len(multi_grid[0]))]) for x in
            range(len(multi_grid)) for z in range(len(multi_grid[0][0]))]


def is_point_in_area(grid: Grid, point: Point) -> bool:
    return (point.x >= 0) and (point.y >= 0) and (point.x < len(grid)) and (point.y < len(grid[0]))


def get_adjacent_points(grid: Grid, point: Point) -> List[Point]:
    possible_points = [
        Point(point.x, point.y - 1), Point(point.x, point.y + 1),
        Point(point.x - 1, point.y), Point(point.x + 1, point.y)
    ]
    return list(filter(lambda p: is_point_in_area(grid, p), possible_points))


def solve_part_1(data: str) -> int:
    grid = parse_data(data)
    path_cost = get_cost_from_to(grid, Point(0, 0), Point(len(grid) - 1, len(grid[0]) - 1))
    return path_cost - grid[0][0]


def solve_part_2(data: str) -> int:
    transform_func = lambda v, x, y: (lambda s: s % 9 if s > 9 else s)(v + x + y)
    grid = transform_grid(parse_data(data), transform_func, 5, 5)
    path_cost = get_cost_from_to(grid, Point(0, 0), Point(len(grid) - 1, len(grid[0]) - 1))
    return path_cost - grid[0][0]


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
