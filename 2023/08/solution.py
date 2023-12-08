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

def part1(s):
    seq, out = parse_input(s)

    pos = 'AAA'
    answer = 0

    while pos != 'ZZZ':
        for side in seq:
            answer += 1
            side = 1 if side == 'R' else 0
            pos = out[pos][side]
            if pos == 'ZZZ':
                break

    lib.aoc.give_answer(2023, 8, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 8)
part1(INPUT)
part2(INPUT)
