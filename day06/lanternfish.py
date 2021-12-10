from collections import Counter
from typing import Dict


def parse_data(data: str) -> Dict[int, int]:
    return dict(Counter(map(int, data.split(","))))


def get_fishes(fishes: Dict[int, int], day_limit: int) -> Dict[int, int]:
    if day_limit == 0:
        return fishes
    fishes_at_day_6 = {6: sum(fishes[day] for day in (0, 7) if fishes.get(day) is not None)}
    old_fishes = {k - 1: v for k, v in fishes.items() if k not in (0, 7)}
    new_fishes = {8: fishes[0]} if fishes.get(0) is not None else {}
    return get_fishes(old_fishes | new_fishes | fishes_at_day_6, day_limit - 1)


def solve_part_1(data: str) -> int:
    return sum(get_fishes(parse_data(data), day_limit=80).values())


def solve_part_2(data: str) -> int:
    return sum(get_fishes(parse_data(data), day_limit=256).values())


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
