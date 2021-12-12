import collections

import lib.aoc

def solve(s, allow_second_visit=False):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        a, b = line.split('-')
        graph[a].append(b)
        graph[b].append(a)

    def gen_paths(pos, seen_small, allow_second_visit):
        for target in graph[pos]:
            if target == 'end':
                yield 1
                continue
            if target == 'start':
                continue
            if target.upper() == target:
                # Big cave, visit as much as we want!
                yield from gen_paths(target, seen_small, allow_second_visit)
            else:
                # Small cave
                if target in seen_small:
                    if allow_second_visit:
                        yield from gen_paths(target, seen_small, False)
                else:
                    seen_small.add(target)
                    yield from gen_paths(target, seen_small, allow_second_visit)
                    seen_small.remove(target)
    return sum(gen_paths('start', set(), allow_second_visit))

def part1(s):
    answer = solve(s)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, True)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 12)
part1(INPUT)
part2(INPUT)
