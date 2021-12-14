from dataclasses import dataclass
from itertools import chain
from typing import List, Tuple, Set, Callable


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def parse_data(data: str) -> List[List[int]]:
    return list(map(lambda r: list(map(int, r)), data.split("\n")))


def flash_all(grid: List[List[int]], already_flashed: Set[Point]) -> List[List[int]]:
    if not can_flash(grid, already_flashed):
        return grid

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] >= 10 and Point(x, y) not in already_flashed:
                already_flashed.add(Point(x, y))
                grid = flash_point(grid, Point(x, y))

    return flash_all(grid, already_flashed)


def flash_point(grid: List[List[int]], point: Point) -> List[List[int]]:
    for point in get_adjacent_points(grid, point):
        grid[point.x][point.y] += 1
    return grid


def increase_energy(grid: List[List[int]]) -> List[List[int]]:
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y] += 1
    return grid


def update_energy(grid: List[List[int]]) -> List[List[int]]:
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] > 9:
                grid[x][y] = 0
    return grid


def next_step(grid: List[List[int]], all_flashes: List[int], total_steps: int,
              stop_rule: Callable[[List[List[int]], int], bool]) -> Tuple[List[List[int]], int, List[int]]:
    if stop_rule(grid, total_steps):
        return grid, total_steps, all_flashes

    new_grid = flash_all(increase_energy(grid), set())
    total_flashes = len(list(filter(lambda v: v >= 10, chain(*new_grid))))
    return next_step(update_energy(new_grid), all_flashes + [total_flashes], total_steps + 1, stop_rule)


def is_point_in_grid(grid: List[List[int]], point: Point) -> bool:
    return (point.x >= 0) and (point.y >= 0) and (point.x < len(grid)) and (point.y < len(grid[0]))


def get_adjacent_points(grid: List[List[int]], point: Point) -> List[Point]:
    possible_points = [
        Point(point.x, point.y - 1), Point(point.x, point.y + 1),
        Point(point.x - 1, point.y), Point(point.x + 1, point.y),
        Point(point.x - 1, point.y - 1), Point(point.x - 1, point.y + 1),
        Point(point.x + 1, point.y - 1), Point(point.x + 1, point.y + 1)
    ]
    return list(filter(lambda p: is_point_in_grid(grid, p), possible_points))


def are_synchronized(grid: List[List[int]]) -> bool:
    return len(set(chain(*grid))) == 1


def can_flash(grid: List[List[int]], already_flashed: Set[Point]) -> bool:
    possible_flashes = {Point(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] >= 10}
    return bool(possible_flashes - already_flashed)


def solve_part_1(data: str) -> int:
    grid = parse_data(data)
    *_, flashes = next_step(grid, [], 0, lambda _, s: s == 100)
    return sum(flashes)


def solve_part_2(data: str) -> int:
    grid = parse_data(data)
    _, total_steps, _ = next_step(grid, [], 0, lambda g, _: are_synchronized(g))
    return total_steps


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
