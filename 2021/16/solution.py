import functools
import operator

import lib.aoc

def parse_bits_impl(bits):
    def pull_raw_bits(n):
        nonlocal bits
        val = bits[:n]
        bits = bits[n:]
        return val
    def pull_bits(n):
        return int(pull_raw_bits(n), 2)

    v = pull_bits(3)
    t = pull_bits(3)
    if t == 4:
        # Literal
        payload = 0
        while True:
            n = pull_bits(5)
            payload = (payload << 4) + (n & 0xF)
            if not n & 0x10:
                break
    else:
        # Operator
        payload = []

        if pull_bits(1):
            count = pull_bits(11)

            for _ in range(count):
                s, bits = parse_bits_impl(bits)
                payload.append(s)
        else:
            sub_len = pull_bits(15)
            sub_bits = pull_raw_bits(sub_len)

            while sub_bits:
                s, sub_bits = parse_bits_impl(sub_bits)
                payload.append(s)

    packet = (v, t, payload)
    return packet, bits

def parse(s):
    bits = bin(int(s, 16))[2:].zfill(len(s)*4)
    packet, _ = parse_bits_impl(bits)
    return packet

def sum_versions(packet):
    v, t, payload = packet
    if t != 4:
        v += sum(map(sum_versions, payload))
    return v

def part1(s):
    answer = sum_versions(parse(s))

    lib.aoc.give_answer(2021, 16, 1, answer)

OPERATORS = [
    sum,
    lambda vals: functools.reduce(operator.mul, vals),
    min,
    max,
    lambda val: val,
    lambda vals: 1 if vals[0] > vals[1] else 0,
    lambda vals: 1 if vals[0] < vals[1] else 0,
    lambda vals: 1 if vals[0] == vals[1] else 0,
]

def eval_packet(p):
    _, t, payload = p
    if isinstance(payload, list):
        payload = list(map(eval_packet, payload))
    return OPERATORS[t](payload)

def part2(s):
    answer = eval_packet(parse(s))

    lib.aoc.give_answer(2021, 16, 2, answer)

INPUT = lib.aoc.get_input(2021, 16)
part1(INPUT)
part2(INPUT)
