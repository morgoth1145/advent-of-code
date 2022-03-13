import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        num, _, start, dims = line.split()
        num = int(num[1:])
        x, y = list(map(int, start[:-1].split(',')))
        w, h = list(map(int, dims.split('x')))
        yield num, x, y, w, h

def part1(s):
    hits = collections.Counter()

    for num, x_start, y_start, w, h in parse_input(s):
        for x in range(x_start, x_start+w):
            for y in range(y_start, y_start+h):
                hits[x,y] += 1

    answer = sum(1 for claims in hits.values()
                 if claims > 1)

    print(f'The answer to part one is {answer}')

def part2(s):
    hits = collections.Counter()

    for num, x_start, y_start, w, h in parse_input(s):
        for x in range(x_start, x_start+w):
            for y in range(y_start, y_start+h):
                hits[x,y] += 1

    answer = sum(1 for claims in hits.values()
                 if claims > 1)

    for num, x_start, y_start, w, h in parse_input(s):
        if all(hits[x,y] == 1
               for x in range(x_start, x_start+w)
               for y in range(y_start, y_start+h)):
            answer = num
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 3)
part1(INPUT)
part2(INPUT)
