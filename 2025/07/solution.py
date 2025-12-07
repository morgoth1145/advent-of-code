import collections

import lib.aoc

def solve(s):
    lines = s.splitlines()

    start = lines[0].index('S')

    split_points = 0
    timelines = {start: 1}

    for l in lines[1:]:
        new_timelines = collections.Counter()

        for x, t in timelines.items():
            if l[x] == '^':
                split_points += 1
                new_timelines[x-1] += t
                new_timelines[x+1] += t
            else:
                new_timelines[x] += t

        timelines = new_timelines

    return split_points, sum(timelines.values())

def part1(s):
    answer, _ = solve(s)

    lib.aoc.give_answer(2025, 7, 1, answer)

def part2(s):
    _, answer = solve(s)

    lib.aoc.give_answer(2025, 7, 2, answer)

INPUT = lib.aoc.get_input(2025, 7)
part1(INPUT)
part2(INPUT)
