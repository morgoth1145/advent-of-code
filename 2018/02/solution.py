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

    lib.aoc.give_answer(2018, 2, 1, answer)

def part2(s):
    ids = list(s.splitlines())

    for idx, a in enumerate(ids):
        for b in ids[idx+1:]:
            diffs = 0
            for c1, c2 in zip(a, b):
                if c1 != c2:
                    diffs += 1
            if diffs == 1:
                for idx, (c1, c2) in enumerate(zip(a, b)):
                    if c1 != c2:
                        answer = a[:idx] + a[idx+1:]
    
    lib.aoc.give_answer(2018, 2, 2, answer)

INPUT = lib.aoc.get_input(2018, 2)
part1(INPUT)
part2(INPUT)
