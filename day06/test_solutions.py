import lanternfish

test_data = """3,4,3,1,2"""


def test_part_1():
    assert lanternfish.solve_part_1(test_data) == 5934


def test_part_2():
    assert lanternfish.solve_part_2(test_data) == 26984457539
