import collections

import lib.aoc

def parse_input(s):
    g = collections.defaultdict(set)

    for line in s.splitlines():
        a, b = line.split('-')
        g[a].add(b)
        g[b].add(a)

    return g

def find_tri_sets(graph):
    res = set()
    for a, connected in graph.items():
        connected = list(connected)
        for i, b in enumerate(connected):
            b_conn = graph[b]
            if a not in b_conn:
                continue
            for c in connected[i+1:]:
                if c not in b_conn:
                    continue
                c_conn = graph[c]
                if a not in c_conn:
                    continue
                if b not in c_conn:
                    continue
                conn = tuple(sorted([a, b, c]))
                res.add(conn)
    return res

def part1(s):
    graph = parse_input(s)

    answer = 0

    for comp_set in find_tri_sets(graph):
        if any(comp.startswith('t')
               for comp in comp_set):
            answer += 1

    lib.aoc.give_answer(2024, 23, 1, answer)

def get_fully_connected(graph, first, rest):
    rest = sorted(rest)

    def impl(group, rest):
        if len(rest) == 0:
            yield list(group)
            return
        for i, other in enumerate(rest):
            if len(group) != len(group & graph[other]):
                continue
            if any(other not in graph[comp]
                   for comp in group):
                continue
            group.add(other)
            yield from impl(group, rest[i+1:])
            group.remove(other)
        yield list(group)

    best = {first}

    for cand in impl({first}, rest):
        if len(cand) > len(best):
            best = cand

    return best

def part2(s):
    graph = parse_input(s)

    best = (-1, None)

    for i, (first, rest) in enumerate(sorted(graph.items(), key=lambda pair:len(pair[1]), reverse=True)):
        if len(rest) + 1 < best[0]:
            break
        group = get_fully_connected(graph, first, rest)
        if len(group) > best[0]:
            best = (len(group), group)

    answer = ','.join(sorted(best[1]))

    lib.aoc.give_answer(2024, 23, 2, answer)

INPUT = lib.aoc.get_input(2024, 23)
part1(INPUT)
part2(INPUT)
