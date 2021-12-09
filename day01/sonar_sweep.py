from typing import List


def parse_data(data: str) -> List[int]:
    return list(map(int, data.split("\n")))


def get_measurements(data: List[int]) -> int:
    zipped = zip(data, data[1:])
    return len(list(filter(lambda t: t[0] < t[1], zipped)))


def get_measurements_sliding_window(data: List[int]) -> int:
    windows = list(map(sum, zip(*(data[i:] for i in range(3)))))
    return get_measurements(windows)


def solve_part_1(data: str) -> int:
    return get_measurements(parse_data(data))


def solve_part_2(data: str) -> int:
    return get_measurements_sliding_window(parse_data(data))


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
