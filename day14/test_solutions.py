import extended_polymerization

test_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def test_part_1():
    assert extended_polymerization.solve_part_1(test_data) == 1588


def test_part_2():
    assert extended_polymerization.solve_part_2(test_data) == 2188189693529
