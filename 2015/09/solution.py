import collections

import lib.aoc

def solve(s, optimize_fn):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        a, _, b, _, dist = line.split()
        dist = int(dist)
        graph[a].append((b, dist))
        graph[b].append((a, dist))

    def impl(path, dist):
        if len(path) == len(graph):
            return dist

        return optimize_fn(impl(path + [neighbor], dist + ndist)
                           for neighbor, ndist in graph[path[-1]]
                           if neighbor not in path)

    return optimize_fn(impl([start], 0)
                       for start in graph.keys())

def part1(s):
    answer = solve(s, min)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, max)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 9)
part1(INPUT)
part2(INPUT)
