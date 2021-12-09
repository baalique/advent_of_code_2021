import dive

test_data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def test_part_1():
    assert dive.solve_part_1(test_data) == 150


def test_part_2():
    assert dive.solve_part_2(test_data) == 900
