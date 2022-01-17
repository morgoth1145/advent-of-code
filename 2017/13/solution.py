import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(':')))

def part1(s):
    answer = 0

    for depth, layers in parse_input(s):
        cycle = 2 * (layers - 1)
        if cycle == 0:
            cycle = 1
        if depth % cycle == 0:
            # Caught!
            answer += depth * layers

    print(f'The answer to part one is {answer}')

def part2(s):
    incongruencies = []

    for depth, layers in parse_input(s):
        cycle = 2 * (layers - 1)
        if cycle == 0:
            cycle = 1
        incongruencies.append((cycle, (cycle - (depth % cycle)) % cycle))

    incongruencies = sorted(incongruencies)

    d = collections.defaultdict(set)
    for mod, bad in incongruencies:
        d[mod].add(bad)

    answer = 0
    while True:
        if all(answer % mod not in bad
               for mod, bad in d.items()):
            break
        answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 13)
part1(INPUT)
part2(INPUT)
