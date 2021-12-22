import re
from dataclasses import dataclass
from itertools import product, chain
from typing import Iterator, List, Tuple


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Velocity:
    x: int
    y: int


@dataclass
class Area:
    p1: Point
    p2: Point


def parse_data(data: str) -> Area:
    regex = r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)"
    x1, x2, y1, y2 = map(int, re.search(regex, data).groups())
    return Area(Point(min(x1, x2), min(y1, y2)), Point(max(x1, x2), max(y1, y2)))


def trajectory(point: Point, velocity: Velocity) -> Iterator[Tuple[Point, Velocity]]:
    while True:
        yield point, velocity
        point = Point(point.x + velocity.x, point.y + velocity.y)
        velocity = velocity_on_next_step(velocity)


def velocity_on_next_step(velocity: Velocity) -> Velocity:
    return Velocity(max(0, velocity.x - 1) if velocity.x >= 0 else min(0, velocity.x + 1), velocity.y - 1)


def is_point_in_area(point: Point, area: Area) -> bool:
    return (area.p1.x <= point.x <= area.p2.x) and (area.p1.y <= point.y <= area.p2.y)


def is_trajectory_never_cross_area(point: Point, velocity: Velocity, area: Area) -> bool:
    return (point.y < area.p1.y and velocity.y <= 0) \
           or (point.x > area.p2.x and velocity.x >= 0) \
           or (point.x < area.p1.x and velocity.x <= 0)


def get_area_crossing_trajectory(point: Point, velocity: Velocity, area: Area) -> None | List[Point]:
    traj = iter(trajectory(point, velocity))
    all_points = []

    while True:
        point, velocity = next(traj)
        all_points.append(point)
        if is_point_in_area(point, area):
            return all_points
        if is_trajectory_never_cross_area(point, velocity, area):
            return


def get_all_trajectories(point: Point, velocities: List[Velocity], area: Area) -> List[List[Point]]:
    return list(
        filter(lambda ps: ps is not None, map(lambda v: get_area_crossing_trajectory(point, v, area), velocities)))


def generate_velocities(min_x: int, max_x: int, min_y: int, max_y: int) -> List[Velocity]:
    return list(map(lambda p: Velocity(*p), product(range(min_x, max_x + 1), range(min_y, max_y + 1))))


def solve_part_1(data: str) -> int:
    area = parse_data(data)
    possible_velocities = generate_velocities(-200, 200, -200, 200)
    crossing_area_trajectories = get_all_trajectories(Point(0, 0), possible_velocities, area)
    max_y = max(map(lambda p: p.y, chain(*crossing_area_trajectories)))
    return max_y


def solve_part_2(data: str) -> int:
    area = parse_data(data)
    possible_velocities = generate_velocities(-200, 200, -200, 200)
    crossing_area_trajectories = get_all_trajectories(Point(0, 0), possible_velocities, area)
    return len(crossing_area_trajectories)


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
