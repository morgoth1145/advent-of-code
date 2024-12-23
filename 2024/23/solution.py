import collections

import lib.aoc

def find_largest_cliques(s, max_clique_size=None):
    net = collections.defaultdict(set)

    for line in s.splitlines():
        a, b = line.split('-')
        net[a].add(b)
        net[b].add(a)

    current_size = 0

    def generate_cliques(group, potential_connections):
        if len(group) + len(potential_connections) < current_size:
            return
        if max_clique_size is not None:
            if len(group) == max_clique_size:
                yield list(group)
                return
            elif len(group) > max_clique_size:
                return
        for i, new_comp in enumerate(potential_connections):
            if (len(group) != len(group & net[new_comp]) or
                any(new_comp not in net[comp]
                    for comp in group)):
                # Not fully connected
                continue
            group.add(new_comp)
            yield from generate_cliques(group, potential_connections[i+1:])
            group.remove(new_comp)
        if len(group) >= current_size:
            yield list(group)

    handled_starts = set()
    cliques = []

    for start, connections in net.items():
        handled_starts.add(start)
        connections = connections - handled_starts
        for clique in generate_cliques({start}, list(connections)):
            if len(clique) > current_size:
                current_size = len(clique)
                cliques = []
            assert(len(clique) == current_size)
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
