from collections import Counter
from dataclasses import dataclass
from typing import List, Iterable, Callable, Optional


@dataclass(frozen=True)
class BinaryRate:
    gamma: int
    epsilon: int


@dataclass(frozen=True)
class LifeSupportRating:
    oxygen_generator_rating: int
    co2_scrubber_rating: int


def parse_data(data: str) -> List[List[bool]]:
    return list(map(lambda row: list(map(lambda c: bool(int(c)), row)), data.split("\n")))


def get_most_common_bits(seq: Iterable[bool]) -> Optional[bool]:
    most_common = Counter(seq).most_common()
    if len(most_common):
        return most_common[0][0]


def reduce_table(table: List[List[bool]], func: Callable[[Iterable[bool]], Optional[bool]]) -> Optional[List[bool]]:
    reduced = list(map(func, zip(*table)))
    if all(map(lambda x: x is not None, reduced)):
        return reduced


def bits_to_int(bits: List[bool]) -> int:
    return int("".join(list(map(lambda x: str(int(x)), bits))), 2)


def get_binary_rate(table: List[List[bool]]) -> Optional[BinaryRate]:
    most_common = reduce_table(table, get_most_common_bits)
    least_common = list(map(lambda b: not b, most_common))
    if most_common and least_common:
        return BinaryRate(gamma=bits_to_int(most_common), epsilon=bits_to_int(least_common))


def filter_bits(table: List[List[bool]], idx: int, func: Callable[[List[List[bool]], int], Optional[bool]]) \
        -> Optional[List[bool]]:
    match table, idx:
        case [row], _:
            return row
        case _, n if n >= len(table[0]):
            return filter_bits(table, 0, func)
        case table, idx:
            matching_bit = func(table, idx)
            if matching_bit is None:
                return
            filtered_table = list(filter(lambda r: r[idx] == matching_bit, table))
            return filter_bits(filtered_table, idx + 1, func)


def get_most_common_or_equal(table: List[List[bool]], idx: int) -> Optional[bool]:
    bits_to_compare = list(map(lambda row: row[idx], table))
    most_common = Counter(bits_to_compare).most_common()

    if not most_common:
        return

    most, least = most_common

    if most[1] == least[1]:
        return True

    return most[0]


def get_least_common_or_equal(table: List[List[bool]], idx: int) -> Optional[bool]:
    bits_to_compare = list(map(lambda row: row[idx], table))
    most_common = Counter(bits_to_compare).most_common()

    if not most_common:
        return

    most, least = most_common

    if most[1] == least[1]:
        return False

    return least[0]


def get_life_support_rating(table: List[List[bool]]) -> Optional[LifeSupportRating]:
    oxygen_generator_rating = filter_bits(table, 0, get_most_common_or_equal)
    co2_scrubber_rating = filter_bits(table, 0, get_least_common_or_equal)
    if oxygen_generator_rating and co2_scrubber_rating:
        return LifeSupportRating(bits_to_int(oxygen_generator_rating), bits_to_int(co2_scrubber_rating))


def solve_part_1(data: str) -> int:
    binary_rate = get_binary_rate(parse_data(data))
    return binary_rate.gamma * binary_rate.epsilon if binary_rate else 0


def solve_part_2(data: str) -> int:
    life_support_rating = get_life_support_rating(parse_data(data))
    return life_support_rating.oxygen_generator_rating * life_support_rating.co2_scrubber_rating \
        if life_support_rating else 0


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
