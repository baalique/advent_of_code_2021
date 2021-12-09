import sonar_sweep

test_data = """199
200
208
210
200
207
240
269
260
263"""


def test_part_1():
    assert sonar_sweep.solve_part_1(test_data) == 7


def test_part_2():
    assert sonar_sweep.solve_part_2(test_data) == 5
