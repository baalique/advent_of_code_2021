import packet_decoder

test_data_1 = "8A004A801A8002F478"
test_data_2 = "620080001611562C8802118E34"
test_data_3 = "C0015000016115A2E0802F182340"
test_data_4 = "A0016C880162017C3686B18A3D4780"
test_data_5 = "C200B40A82"
test_data_6 = "04005AC33890"
test_data_7 = "880086C3E88112"
test_data_8 = "CE00C43D881120"
test_data_9 = "D8005AC2A8F0"
test_data_10 = "F600BC2D8F"
test_data_11 = "9C005AC2F8F0"
test_data_12 = "9C0141080250320F1802104A08"


def test_part_1():
    assert packet_decoder.solve_part_1(test_data_1) == 16
    assert packet_decoder.solve_part_1(test_data_2) == 12
    assert packet_decoder.solve_part_1(test_data_3) == 23
    assert packet_decoder.solve_part_1(test_data_4) == 31


def test_part_2():
    assert packet_decoder.solve_part_2(test_data_5) == 3
    assert packet_decoder.solve_part_2(test_data_6) == 54
    assert packet_decoder.solve_part_2(test_data_7) == 7
    assert packet_decoder.solve_part_2(test_data_8) == 9
    assert packet_decoder.solve_part_2(test_data_9) == 1
    assert packet_decoder.solve_part_2(test_data_10) == 0
    assert packet_decoder.solve_part_2(test_data_11) == 0
    assert packet_decoder.solve_part_2(test_data_12) == 1
