import collections

import lib.aoc

def parse(s):
    out = []
    for l in s.split('\n'):
        a, b = l.split(' -> ')
        a = list(map(int, a.split(',')))
        b = list(map(int, b.split(',')))
        out.append((a, b))
    return out

def part1(s):
    lines = parse(s)

    touched = collections.defaultdict(int)

    for start, end in lines:
        x0,y0 = start
        x1,y1 = end
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1)+1):
                touched[(x0, y)] += 1
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1)+1):
                touched[(x, y0)] += 1

    answer = 0

    for val in touched.values():
        if val > 1:
            answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 5)
part1(INPUT)
part2(INPUT)
