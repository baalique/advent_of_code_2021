import hydrothermal_venture

test_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


def test_part_1():
    assert hydrothermal_venture.solve_part_1(test_data) == 5


def test_part_2():
    assert hydrothermal_venture.solve_part_2(test_data) == 12
