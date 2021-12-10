import the_treachery_of_whales

test_data = """16,1,2,0,4,2,7,1,2,14"""


def test_part_1():
    assert the_treachery_of_whales.solve_part_1(test_data) == 37


def test_part_2():
    assert the_treachery_of_whales.solve_part_2(test_data) == 168
