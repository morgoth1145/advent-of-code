import collections

import lib.aoc

def part1(s):
    twice = 0
    thrice = 0

    for line in s.splitlines():
        c = collections.Counter(line)
        if 3 in c.values():
            thrice += 1
        if 2 in c.values():
            twice += 1

    answer = twice * thrice

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 2)
part1(INPUT)
part2(INPUT)
