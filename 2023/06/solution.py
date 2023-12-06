import math
import parse

import lib.aoc

def parse_all_ints(s):
    return list(map(lambda r:r[0], parse.findall('{:d}', s)))

def parse_input(s):
    for line in s.splitlines():
        yield parse_all_ints(line)

def ways_to_beat(time, dist):
    ways = 0

    for t in range(1, time):
        rem = time - t
        if rem * t > dist:
            ways += 1

    return ways

def part1(s):
    times, distances = parse_input(s)

    answer = math.prod(ways_to_beat(t, d) for t, d in zip(times, distances))

    lib.aoc.give_answer(2023, 6, 1, answer)

def part2(s):
    s = s.replace(' ', '')
    time, dist = parse_all_ints(s)

    answer = ways_to_beat(time, dist)

    lib.aoc.give_answer(2023, 6, 2, answer)

INPUT = lib.aoc.get_input(2023, 6)
part1(INPUT)
part2(INPUT)
