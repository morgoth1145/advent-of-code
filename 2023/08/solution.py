import math

import lib.aoc

def parse_input(s):
    groups = s.split('\n\n')

    seq, b = groups

    out = {}

    for line in b.splitlines():
       a, b = line.split(' = ')
       b = b.replace('(', '').replace(')', '')
       b, c = b.split(', ')
       out[a] = (b, c)

    return seq, out

def count_steps(seq, mapping, pos, end_fn):
    steps = 0

    while True:
        for side in seq:
            steps += 1
            side = 1 if side == 'R' else 0
            pos = mapping[pos][side]
            if end_fn(pos):
                return steps

def part1(s):
    seq, out = parse_input(s)

    answer = count_steps(seq, out, 'AAA', lambda pos: pos == 'ZZZ')

    lib.aoc.give_answer(2023, 8, 1, answer)

def part2(s):
    seq, mapping = parse_input(s)

    positions = []
    for pos in mapping:
        if pos[-1] == 'A':
            positions.append(pos)

    min_steps = [count_steps(seq, mapping, pos, lambda pos: pos[-1] == 'Z')
                 for pos in positions]

    # Wait, this is right?! That's hilarous!
    answer = math.lcm(*min_steps)

    lib.aoc.give_answer(2023, 8, 2, answer)

INPUT = lib.aoc.get_input(2023, 8)
part1(INPUT)
part2(INPUT)
