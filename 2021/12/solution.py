import collections

import lib.aoc

def parse(s):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        a, b = line.split('-')
        graph[a].append(b)
        graph[b].append(a)
    return graph

def count_paths(graph):
    def impl(path, seen_small):
        if path[-1] == 'end':
            yield 1
            return
        for target in graph[path[-1]]:
            if target in seen_small:
                continue
            if target.upper() != target:
                seen_small.add(target)
                yield from impl(path + [target], seen_small)
                seen_small.remove(target)
            else:
                yield from impl(path + [target], seen_small)
    return sum(1 for _ in impl(['start'], {'start'}))

def part1(s):
    graph = parse(s)

    answer = count_paths(graph)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 12)
part1(INPUT)
part2(INPUT)
