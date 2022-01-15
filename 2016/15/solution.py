import parse

import lib.aoc
import lib.math

def parse_discs(s):
    for line in s.splitlines():
        _, positions, _, start = list(map(lambda r:r[0], parse.findall('{:d}', line)))
        yield positions, start

def part1(s):
    congruencies = []
    for idx, (positions, start) in enumerate(parse_discs(s)):
        congruencies.append((positions, start+idx+1))

    answer = lib.math.offset_chinese_remainder(congruencies)

    print(f'The answer to part one is {answer}')

def part2(s):
    congruencies = []
    for idx, (positions, start) in enumerate(parse_discs(s)):
        congruencies.append((positions, start+idx+1))
    congruencies.append((11, len(congruencies)+1))

    answer = lib.math.offset_chinese_remainder(congruencies)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 15)
part1(INPUT)
part2(INPUT)
