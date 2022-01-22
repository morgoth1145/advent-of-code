import parse

import lib.aoc

def gen_sequence(prev, fact, mod):
    while True:
        val = (prev * fact) % mod
        yield val
        prev = val

def part1(s):
    a, b = list(map(lambda r:r[0], parse.findall('{:d}', s)))

    a_vals = gen_sequence(a, 16807, 2147483647)
    b_vals = gen_sequence(b, 48271, 2147483647)

    BIT_MASK = 0xFFFF # 16 bits

    answer = 0

    for _ in range(40000000):
        if next(a_vals) & BIT_MASK == next(b_vals) & BIT_MASK:
            answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 15)
part1(INPUT)
part2(INPUT)
