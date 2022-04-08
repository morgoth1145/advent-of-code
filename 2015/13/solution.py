import collections

import lib.aoc

def parse_input(s):
    pairs = collections.Counter()

    for line in s.splitlines():
        a, _, change, n, _, _, _, _, _, _, b = line.split()
        assert(b[-1] == '.')
        b = b[:-1]
        n = int(n)
        if change == 'lose':
            n = -n
        else:
            assert(change == 'gain')
        pairs[min(a,b), max(a,b)] += n

    graph = collections.defaultdict(list)

    for (a,b), n in pairs.items():
        graph[a].append((b, n))
        graph[b].append((a, n))

    return graph

def best_path(graph):
    def impl(start, path, cost):
        if len(path) == len(graph) and path[-1] == start:
            yield cost
            return

        current = start if len(path) == 0 else path[-1]

        for neighbor, diff in graph[current]:
            if neighbor in path:
                continue

            yield from impl(start, path + [neighbor], cost + diff)

    return max(max(impl(start, [], 0))
               for start in graph.keys())

def part1(s):
    graph = parse_input(s)
    answer = best_path(graph)

    lib.aoc.give_answer(2015, 13, 1, answer)

def part2(s):
    graph = parse_input(s)

    assert('me' not in graph.keys())
    for person in list(graph.keys()):
        graph['me'].append((person, 0))
        graph[person].append(('me', 0))

    answer = best_path(graph)

    lib.aoc.give_answer(2015, 13, 2, answer)

INPUT = lib.aoc.get_input(2015, 13)
part1(INPUT)
part2(INPUT)
