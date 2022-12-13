import functools
import json

import lib.aoc

def parse_packets_as_flat_list(s):
    return map(json.loads, s.replace('\n\n', '\n').splitlines())

def packet_cmp(a, b):
    for aval, bval in zip(a, b):
        if isinstance(aval, int):
            if isinstance(bval, int):
                if aval < bval:
                    return -1
                if aval > bval:
                    return 1
                continue
            # bval is a list, make aval a list to match for subsequent checks
            aval = [aval]

        # aval is a list
        if isinstance(bval, int):
            bval = [bval]

        subcmp = packet_cmp(aval, bval)
        if subcmp != 0:
            return subcmp

    if len(a) < len(b):
        return -1
    if len(b) < len(a):
        return 1
    return 0

def part1(s):
    packets = list(parse_packets_as_flat_list(s))

    answer = sum(i+1
                 for i, (a, b)
                 in enumerate(zip(packets[::2], packets[1::2]))
                 if packet_cmp(a, b) == -1)

    lib.aoc.give_answer(2022, 13, 1, answer)

def part2(s):
    packets = list(parse_packets_as_flat_list(s)) + [[[2]], [[6]]]
    packets.sort(key=functools.cmp_to_key(packet_cmp))

    answer = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)

    lib.aoc.give_answer(2022, 13, 2, answer)

INPUT = lib.aoc.get_input(2022, 13)
part1(INPUT)
part2(INPUT)
