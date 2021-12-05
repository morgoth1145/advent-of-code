import collections

import lib.aoc

def count_coord_hits(s, include_diagonals):
    coord_hits = collections.Counter()

    for l in s.split('\n'):
        a, b = l.split(' -> ')
        x0,y0 = list(map(int, a.split(',')))
        x1,y1 = list(map(int, b.split(',')))

        # Any diagonals are 45 degrees so dx/dy are simple!
        dx = 1 if x1>x0 else -1
        if x0 == x1:
            dx = 0
        dy = 1 if y1>y0 else -1
        if y0 == y1:
            dy = 0

        if dx != 0 and dy != 0 and not include_diagonals:
            continue

        x = x0
        y = y0

        coord_hits[x,y] += 1
        while x != x1 or y != y1:
            x += dx
            y += dy
            coord_hits[x,y] += 1

    return sum(hits > 1 for hits in coord_hits.values())

def part1(s):
    answer = count_coord_hits(s, include_diagonals=False)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = count_coord_hits(s, include_diagonals=True)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 5)
part1(INPUT)
part2(INPUT)
