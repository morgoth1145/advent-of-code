import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(',')))

def part1(s):
    data = list(parse_input(s))

    links = collections.defaultdict(set)

    for i, (x, y, z, w) in enumerate(data):
        for j, (x2, y2, z2, w2) in enumerate(data):
            dist = abs(x-x2) + abs(y-y2) + abs(z-z2) + abs(w-w2)
            if dist <= 3:
                links[i].add(j)

    answer = 0
    handled = set()

    for i in range(len(data)):
        if i in handled:
            continue

        answer += 1

        to_handle = [i]
        while to_handle:
            i = to_handle.pop(-1)
            handled.add(i)

            for j in links[i]:
                if j not in handled:
                    to_handle.append(j)

    lib.aoc.give_answer(2018, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2018, 25)
part1(INPUT)
part2(INPUT)
