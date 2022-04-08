import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        num, _, start, dims = line.split()
        num = int(num[1:])
        x_start, y_start = list(map(int, start[:-1].split(',')))
        w, h = list(map(int, dims.split('x')))

        coords = [(x, y)
                  for x in range(x_start, x_start+w)
                  for y in range(y_start, y_start+h)]

        yield num, coords

def part1(s):
    hits = collections.Counter()

    for num, coords in parse_input(s):
        for c in coords:
            hits[c] += 1

    answer = sum(1 for claims in hits.values()
                 if claims > 1)

    lib.aoc.give_answer(2018, 3, 1, answer)

def part2(s):
    hits = collections.Counter()

    for num, coords in parse_input(s):
        for c in coords:
            hits[c] += 1

    for num, coords in parse_input(s):
        if all(hits[c] == 1 for c in coords):
            answer = num
            break

    lib.aoc.give_answer(2018, 3, 2, answer)

INPUT = lib.aoc.get_input(2018, 3)
part1(INPUT)
part2(INPUT)
