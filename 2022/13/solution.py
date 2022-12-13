import functools
import json

import lib.aoc

def parse_packets_as_flat_list(s):
    return map(json.loads, s.replace('\n\n', '\n').splitlines())

def packet_cmp(a, b):
    match a, b:
        case int(), int(): return -1 if a < b else 1 if a > b else 0
        case list(), int(): return packet_cmp(a, [b])
        case int(), list(): return packet_cmp([a], b)
        case [], []: return 0
        case [], list(): return -1
        case list(), []: return 1
        case [a, *rest_a], [b, *rest_b]: return (packet_cmp(a, b)
                                                 or packet_cmp(rest_a, rest_b))

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
