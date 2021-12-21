import operator
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple

BitData = List[int]


@dataclass
class LiteralValue:
    value: int


@dataclass
class Operator:
    type_id: int
    sub_packets: List["Packet"]


@dataclass
class Packet:
    version: int
    type_id: int
    data: LiteralValue | Operator


class PacketError(Exception):
    pass


def parse_data(data: str) -> BitData:
    return list(map(int, reduce(operator.add, map(lambda c: bin(int(c, 16))[2:].zfill(4), data), "")))


def parse_packet(data: BitData) -> Tuple[Packet | None, BitData]:
    if not data:
        return None, []
    version = to_decimal(data[:3])
    type_id = to_decimal(data[3:6])

    if type_id == 4:
        packet_data, rest = parse_value(data[6:])
    else:
        packet_data, rest = parse_operator(data[6:])
    return Packet(version, type_id, packet_data), rest


def parse_value(data: BitData) -> Tuple[LiteralValue, BitData]:
    bits = []
    idx = 0
    while True:
        bits.extend(data[idx + 1: idx + 5])
        if data[idx] == 0:
            return LiteralValue(to_decimal(bits)), data[idx + 5:]
        else:
            idx += 5


def parse_operator(data: BitData) -> Tuple[Operator, BitData]:
    if data[0] == 0:
        total_length = to_decimal(data[1:16])
        packets, rest = parse_packets_from_length(data[16:], total_length)
        return Operator(0, packets), rest
    packets_count = to_decimal(data[1:12])
    packets, rest = parse_multiple_packets(data[12:], packets_count)
    return Operator(1, packets), rest


def parse_packets_from_length(data: BitData, total_length: int) -> Tuple[List[Packet], BitData]:
    cur_length = 0
    packets = []

    while True:
        if cur_length >= total_length:
            return packets, data
        cur, rest = parse_packet(data)
        packets.append(cur)
        cur_length += len(data) - len(rest)
        data = rest


def parse_multiple_packets(data: BitData, packets_count: int) -> Tuple[List[Packet], BitData]:
    total_packets = 0
    packets = []

    while True:
        if total_packets == packets_count:
            return packets, data
        cur, data = parse_packet(data)
        packets.append(cur)
        total_packets += 1


def get_sum_of_all_versions(packet: Packet) -> int:
    match packet.data:
        case LiteralValue(_):
            return packet.version
        case Operator(_, sub_packets):
            return packet.version + sum(map(get_sum_of_all_versions, sub_packets))


def eval_packet(packet: Packet) -> int:
    match packet.type_id:
        case 0:
            return sum(map(eval_packet, packet.data.sub_packets))
        case 1:
            return reduce(operator.mul, map(eval_packet, packet.data.sub_packets))
        case 2:
            return min(map(eval_packet, packet.data.sub_packets))
        case 3:
            return max(map(eval_packet, packet.data.sub_packets))
        case 4:
            return packet.data.value
        case 5:
            return int(eval_packet(packet.data.sub_packets[0]) > eval_packet(packet.data.sub_packets[1]))
        case 6:
            return int(eval_packet(packet.data.sub_packets[0]) < eval_packet(packet.data.sub_packets[1]))
        case 7:
            return int(eval_packet(packet.data.sub_packets[0]) == eval_packet(packet.data.sub_packets[1]))
        case _:
            raise PacketError


def to_decimal(bits: BitData) -> int:
    return int(reduce(lambda acc, x: acc + str(x), bits, ""), 2)


def solve_part_1(data: str) -> int:
    packet, _ = parse_packet(parse_data(data))
    return get_sum_of_all_versions(packet)


def solve_part_2(data: str) -> int:
    packet, _ = parse_packet(parse_data(data))
    return eval_packet(packet)


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
