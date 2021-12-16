import re
from collections import Counter
from functools import reduce
from typing import Tuple, Dict

Polymer = Dict[str, int]
PolymerPairs = Dict[Tuple[str, str], int]
InsertionRules = Dict[Tuple[str, str], str]


def parse_data(data: str) -> Tuple[PolymerPairs, InsertionRules]:
    seq, rules = data.split("\n\n")
    pairs = (lambda s: list(zip(s, s[1:])))(list(seq))
    return dict(Counter(pairs)), reduce(lambda acc, x: acc | parse_rule(x), rules.split("\n"), {})


def parse_rule(row: str) -> InsertionRules:
    regex = r"([A-Z])([A-Z]) -> ([A-Z])"
    first, second, res = re.search(regex, row).groups()
    return {(first, second): res}


def insert_polymers(polymer: PolymerPairs, rules: InsertionRules) -> PolymerPairs:
    return reduce(
        lambda acc, x: merge_dicts(acc, merge_dicts({(x[0][0], rules[x[0]]): x[1]}, {(rules[x[0]], x[0][1]): x[1]})),
        polymer.items(), {})


def repeat_inserting_polymers(polymer: PolymerPairs, rules: InsertionRules, limit: int) -> PolymerPairs:
    return reduce(lambda acc, _: insert_polymers(acc, rules), range(limit), polymer)


def pairs_to_single(polymer: PolymerPairs) -> Polymer:
    first = reduce(lambda acc, x: merge_dicts(acc, {x[0]: polymer[x]}), polymer, {})
    second = reduce(lambda acc, x: merge_dicts(acc, {x[1]: polymer[x]}), polymer, {})
    return {k: (v + 1) // 2 for k, v in merge_dicts(first, second).items()}


def merge_dicts(d1: dict, d2: dict) -> dict:
    return {k: d1.get(k, 0) + d2.get(k, 0) for k in set(d1.keys()) | set(d2.keys())}


def solve_part_1(data: str) -> int:
    poly, rules = parse_data(data)
    result_poly = pairs_to_single(repeat_inserting_polymers(poly, rules, 10))
    return max(result_poly.values()) - min(result_poly.values())


def solve_part_2(data: str) -> int:
    poly, rules = parse_data(data)
    result_poly = pairs_to_single(repeat_inserting_polymers(poly, rules, 40))
    return max(result_poly.values()) - min(result_poly.values())


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
