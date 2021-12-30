import parse

import lib.aoc

def part1(s):
    answer = sum(map(lambda r:r[0], parse.findall('{:d}', s)))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 12)
part1(INPUT)
part2(INPUT)
