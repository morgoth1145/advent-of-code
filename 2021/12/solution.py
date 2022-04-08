import collections

import lib.aoc

def solve(s, allow_second_visit=False):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        a, b = line.split('-')
        graph[a].append(b)
        graph[b].append(a)

    def gen_paths(pos, seen, allow_second_visit):
        for target in graph[pos]:
            if target == 'end':
                yield 1
                continue
            if target == 'start':
                continue
            if target.islower() and target in seen:
                if allow_second_visit:
                    yield from gen_paths(target, seen, False)
                continue
            yield from gen_paths(target, seen | {target}, allow_second_visit)

    return sum(gen_paths('start', set(), allow_second_visit))

def part1(s):
    answer = solve(s)
    lib.aoc.give_answer(2021, 12, 1, answer)

def part2(s):
    answer = solve(s, True)
    lib.aoc.give_answer(2021, 12, 2, answer)

INPUT = lib.aoc.get_input(2021, 12)
part1(INPUT)
part2(INPUT)
