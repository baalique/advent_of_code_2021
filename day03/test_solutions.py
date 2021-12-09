import binary_diagnostic

test_data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def test_part_1():
    assert binary_diagnostic.solve_part_1(test_data) == 198


def test_part_2():
    assert binary_diagnostic.solve_part_2(test_data) == 230
