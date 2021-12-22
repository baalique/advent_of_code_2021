import trick_shot

test_data = """target area: x=20..30, y=-10..-5"""


def test_part_1():
    assert trick_shot.solve_part_1(test_data) == 45


def test_part_2():
    assert trick_shot.solve_part_2(test_data) == 112
