import smoke_basin

test_data = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_part_1():
    assert smoke_basin.solve_part_1(test_data) == 15


def test_part_2():
    assert smoke_basin.solve_part_2(test_data) == 1134
