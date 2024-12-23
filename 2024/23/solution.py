import collections

import lib.aoc

def find_largest_cliques(s, max_clique_size=None):
    net = collections.defaultdict(set)

    for line in s.splitlines():
        a, b = line.split('-')
        net[a].add(b)
        net[b].add(a)

    current_size = 0

    def generate_cliques(group, candidates):
        if len(group) + len(candidates) < current_size:
            return
        if max_clique_size is not None:
            if len(group) == max_clique_size:
                yield list(group)
                return
        for new_comp in list(candidates):
            candidates.remove(new_comp)
            connections = net[new_comp]
            if len(group) != len(group & connections):
                continue
            group.add(new_comp)
            yield from generate_cliques(group, candidates & connections)
            group.remove(new_comp)
        if len(group) >= current_size:
            yield list(group)

    cliques = []

    for clique in generate_cliques(set(), set(net)):
        if len(clique) > current_size:
            current_size = len(clique)
            cliques = []
        cliques.append(clique)

    return cliques

def part1(s):
    answer = sum(any(comp[0] == 't'
                     for comp
                     in clique)
                 for clique
                 in find_largest_cliques(s, max_clique_size=3))

    lib.aoc.give_answer(2024, 23, 1, answer)

def part2(s):
    options = list(find_largest_cliques(s))
    assert(len(options) == 1)

    answer = ','.join(sorted(options[0]))

    lib.aoc.give_answer(2024, 23, 2, answer)

INPUT = lib.aoc.get_input(2024, 23)
part1(INPUT)
part2(INPUT)
