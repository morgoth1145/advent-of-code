import itertools

import lib.aoc

def part1(s):
    a, b = map(int, s.splitlines())

    cracking_val = 1
    mod = 20201227
    for exp in itertools.count():
        if cracking_val == a:
            base = b
            break
        if cracking_val == b:
            base = a
            break
        cracking_val = (cracking_val * 7) % mod

    answer = pow(base, exp, mod)
    lib.aoc.give_answer(2020, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2020, 25)

part1(INPUT)
part2(INPUT)
