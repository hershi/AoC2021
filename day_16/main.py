#!/usr/bin/env python3
from enum import Enum
from functools import reduce


VERSION_SIZE = 3
TYPE_SIZE = 3
LENGTH_TYPE_SIZE = 1


class BitStream:
    def __init__(self, input_string):
        self.bytes = [int("".join(c), 16) for c in zip(*[iter(input_string)]*2)]


    def get_bits(self, start, end):
        start_byte = start // 8
        end_byte = end // 8

        shift = 8 - (end % 8)
        prefix_drop = start % 8

        bytes = self.bytes[start_byte:end_byte + 1]
        bytes[0] &= 0xFF >> prefix_drop

        return int.from_bytes(bytes, byteorder='big', signed=False) >> shift


    def __str__(self):
        return ''.join([f'{b:08b}' for b in self.bytes])


class LengthType(Enum):
    TOTAL_LENGTH=0
    NUM_PACKETS=1


class Operators(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUALS = 7

class Parser():
    def __init__(self, bit_stream):
        self.bit_stream = bit_stream
        self.pos = 0


    def read_bits(self, size):
        self.pos += size
        return self.bit_stream.get_bits(self.pos - size, self.pos)


    def read_literal(self):
        value = 0
        is_last = False
        i = 0
        while not is_last:
            is_last = self.read_bits(1) == 0
            value = (value << 4) + self.read_bits(4)
            i+=1

        return value


class Packet():
    def __init__(self, version, is_compound):
        self.version = version
        self.is_compound = is_compound


class LiteralPacket(Packet):
    def __init__(self, version, bit_stream):
        super().__init__(version, False)
        self.value = bit_stream.read_literal()

    def val(self):
        return self.value


class CompoundPacket(Packet):
    def __init__(self, version, packet_type_id, bit_stream):
        super().__init__(version, True)
        self.operator = Operators(packet_type_id)

        length_type = LengthType(bit_stream.read_bits(LENGTH_TYPE_SIZE))

        if length_type == LengthType.NUM_PACKETS:
            return self._parse_by_num_packets(bit_stream)

        return self._parse_by_total_length(bit_stream)


    def _parse_by_num_packets(self, bit_stream):
        num_sub_packets = bit_stream.read_bits(11)
        self.sub_packets = [parse_packet(bit_stream) for i in range(num_sub_packets)]


    def _parse_by_total_length(self, bit_stream):
        total_length = bit_stream.read_bits(15)

        start_pos = bit_stream.pos

        self.sub_packets = []
        while bit_stream.pos - start_pos < total_length:
            self.sub_packets.append(parse_packet(bit_stream))

        assert(bit_stream.pos == start_pos + total_length)


    def val(self):
        sub_packets_values = [p.val() for p in self.sub_packets]
        if self.operator == Operators.SUM:
            return sum(sub_packets_values)
        elif self.operator == Operators.PRODUCT:
            return reduce(lambda x,y:x*y, sub_packets_values)
        elif self.operator == Operators.MINIMUM:
            return min(sub_packets_values)
        elif self.operator == Operators.MAXIMUM:
            return max(sub_packets_values)
        elif self.operator == Operators.GREATER_THAN:
            return int(sub_packets_values[0] > sub_packets_values[1])
        elif self.operator == Operators.LESS_THAN:
            return int(sub_packets_values[0] < sub_packets_values[1])
        else: #  self.operator == Operators.EQUALS
            return int(sub_packets_values[0] == sub_packets_values[1])


def parse_packet(bit_stream):
    version = bit_stream.read_bits(VERSION_SIZE)
    packet_type_id = bit_stream.read_bits(TYPE_SIZE)
    if packet_type_id == 4:
        return LiteralPacket(version, bit_stream)
    else:
        return CompoundPacket(version, packet_type_id, bit_stream)


def read_input(multiplier=1):
    with open('./input.txt', 'r') as input_file:
        return BitStream(input_file.readlines()[0].strip())


def visit_packets(context, packet, f):
    context = f(context, packet)

    if packet.is_compound:
        for packet in packet.sub_packets:
            context = visit_packets(context, packet, f)

    return context

def part_1(packet):
    res = visit_packets(0, packet, lambda c,p: c+p.version)
    print(res)


def part_2(packet):
    print(packet.val())


packet = parse_packet(Parser(read_input()))
part_1(packet)
part_2(packet)


