import parse

import lib.aoc

def gen_sequence(prev, fact, mod):
    while True:
        val = (prev * fact) % mod
        yield val
        prev = val

def judge(a_seq, b_seq, to_check):
    matched = 0
    BIT_MASK = 0xFFFF # 16 bits

    for _ in range(to_check):
        if next(a_seq) & BIT_MASK == next(b_seq) & BIT_MASK:
            matched += 1

    return matched

def part1(s):
    a, b = list(map(lambda r:r[0], parse.findall('{:d}', s)))

    a_seq = gen_sequence(a, 16807, 2147483647)
    b_seq = gen_sequence(b, 48271, 2147483647)

    answer = judge(a_seq, b_seq, 40000000)

    print(f'The answer to part one is {answer}')

def part2(s):
    a, b = list(map(lambda r:r[0], parse.findall('{:d}', s)))

    a_seq = gen_sequence(a, 16807, 2147483647)
    b_seq = gen_sequence(b, 48271, 2147483647)

    a_seq = filter(lambda val: val & 3 == 0, a_seq)
    b_seq = filter(lambda val: val & 7 == 0, b_seq)

    answer = judge(a_seq, b_seq, 5000000)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 15)
part1(INPUT)
part2(INPUT)
