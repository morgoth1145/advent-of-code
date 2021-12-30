import collections

import lib.aoc

def parse_input(s):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        a, _, b, _, dist = line.split()
        dist = int(dist)
        graph[a].append((b, dist))
        graph[b].append((a, dist))
    return graph

def best_hamiltonian_path(start, graph):
    def impl(path, dist):
        if len(path) == len(graph):
            return path, dist

        best = None

        for neighbor, ndist in graph[path[-1]]:
            if neighbor in path:
                continue
            attempt = impl(path + [neighbor], dist + ndist)
            if best is None or best[1] > attempt[1]:
                best = attempt

        return best

    return impl([start], 0)

def part1(s):
    graph = parse_input(s)

    best = None

    for start in graph.keys():
        path, dist = best_hamiltonian_path(start, graph)
        if best is None or best > dist:
            best = dist

    answer = best

    print(f'The answer to part one is {answer}')

def worst_hamiltonian_path(start, graph):
    def impl(path, dist):
        if len(path) == len(graph):
            return path, dist

        best = None

        for neighbor, ndist in graph[path[-1]]:
            if neighbor in path:
                continue
            attempt = impl(path + [neighbor], dist + ndist)
            if best is None or best[1] < attempt[1]:
                best = attempt

        return best

    return impl([start], 0)

def part2(s):
    graph = parse_input(s)

    best = None

    for start in graph.keys():
        path, dist = worst_hamiltonian_path(start, graph)
        if best is None or best < dist:
            best = dist

    answer = best

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 9)
part1(INPUT)
part2(INPUT)
