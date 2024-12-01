import collections

import lib.aoc

def parse_input(s):
    a = []
    b = []

    for line in s.splitlines():
        an, bn = line.split()
        a.append(int(an))
        b.append(int(bn))

    return a, b

def part1(s):
    a, b = parse_input(s)

    answer = sum(abs(an-bn)
                 for an, bn
                 in zip(sorted(a), sorted(b)))

    lib.aoc.give_answer(2024, 1, 1, answer)

def part2(s):
    a, b = parse_input(s)

    ac = collections.Counter(a)
    bc = collections.Counter(b)

    answer = sum(v * an * bc[v]
                 for v, an
                 in ac.items())

    lib.aoc.give_answer(2024, 1, 2, answer)

INPUT = lib.aoc.get_input(2024, 1)
part1(INPUT)
part2(INPUT)
