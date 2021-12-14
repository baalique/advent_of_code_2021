import dumbo_octopus

test_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_part_1():
    assert dumbo_octopus.solve_part_1(test_data) == 1656


def test_part_2():
    assert dumbo_octopus.solve_part_2(test_data) == 195
