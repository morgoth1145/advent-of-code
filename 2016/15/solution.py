import lib.aoc
import lib.math

def parse_congruencies(s):
    for idx, line in enumerate(s.splitlines()):
        parts = line.split()
        yield int(parts[3]), int(parts[11][:-1]) + idx + 1

def part1(s):
    answer = lib.math.offset_chinese_remainder(parse_congruencies(s))

    lib.aoc.give_answer(2016, 15, 1, answer)

def part2(s):
    s += '\nDisc n+1 has 11 positions; at time=0, it is at position 0.'

    answer = lib.math.offset_chinese_remainder(parse_congruencies(s))

    lib.aoc.give_answer(2016, 15, 2, answer)

INPUT = lib.aoc.get_input(2016, 15)
part1(INPUT)
part2(INPUT)
