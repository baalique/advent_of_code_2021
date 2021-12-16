import passage_pathing

test_data_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
test_data_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
test_data_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def test_part_1():
    assert passage_pathing.solve_part_1(test_data_1) == 10
    assert passage_pathing.solve_part_1(test_data_2) == 19
    assert passage_pathing.solve_part_1(test_data_3) == 226


def test_part_2():
    assert passage_pathing.solve_part_2(test_data_1) == 36
    assert passage_pathing.solve_part_2(test_data_2) == 103
    assert passage_pathing.solve_part_2(test_data_3) == 3509
