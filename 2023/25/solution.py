import networkx

import lib.aoc

def parse_graph(s):
    g = networkx.Graph()

    for line in s.splitlines():
        src, dests = line.split(': ')
        for d in dests.split():
            g.add_edge(src, d, capacity=1)

    return g

def solve_via_plot(s):
    import matplotlib.pyplot as plt

    g = parse_graph(s)

    networkx.draw(g, with_labels=True)
    plt.show()

    for idx in range(3):
        src = input(f'Source node {idx+1}: ')
        dest = input(f'Destination node {idx+1}: ')

        g.remove_edge(src, dest)

    networkx.draw(g, with_labels=True)
    plt.show()

def solve(s):
    g = parse_graph(s)

    nodes = list(g)

    for idx, n1 in enumerate(nodes):
        for n2 in nodes[idx+1:]:
            num_cuts, (left, right) = networkx.minimum_cut(g, n1, n2)
            if num_cuts == 3:
                return len(left) * len(right)

def solve2(s):
    import collections

    g = collections.defaultdict(set)

    for line in s.splitlines():
        src, dests = line.split(': ')
        for d in dests.split():
            g[src].add(d)
            g[d].add(src)

    triangles = set()

    for node in g:
        for n in g[node]:
            for n2 in g[n]:
                if node in g[n2]:
                    triangles.add(tuple(sorted((node, n, n2))))

    triangles = sorted(triangles)

    seeds = sorted(triangles)

    seeds = list(g)

    answers = []

    while seeds:
        start = seeds.pop()

        if len(seeds) % 100 == 0:
            print(len(seeds))

        unconnected = {n:0 for n in set(g) - {start}}

        for n in g[start]:
            if n in unconnected:
                unconnected[n] += 1

        while unconnected and sum(unconnected.values()) != 3:
            node, c = max(unconnected.items(), key=lambda p: p[1])
##            print(start, node, c)

            unconnected.pop(node)

            for n in g[node]:
                if n in unconnected:
                    unconnected[n] += 1

        if set(unconnected.values()) - {0} == {1}:
            answers.append(len(unconnected) * (len(g) - len(unconnected)))
            continue

##        print('Not a valid split',
##              start,
##              len(unconnected),
##              sum(unconnected.values()),
##              len(seeds))

    if len(answers) > 0:
        assert(len(set(answers)) == 1)
        print(f'{len(answers)} found out of {len(g)} tries ({100*len(answers)/len(g)}% success rate)')
        return answers[0]

    print('No soulution?!')

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2023, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2023, 25)
part1(INPUT)
part2(INPUT)

##INPUT = '''jqt: rhn xhk nvd
##rsh: frs pzl lsr
##xhk: hfx
##cmg: qnr nvd lhk bvb
##rhn: xhk bvb hfx
##bvb: xhk hfx
##pzl: lsr hfx nvd
##qnr: nvd
##ntq: jqt hfx bvb xhk
##nvd: lhk
##lsr: lhk
##rzs: qnr cmg lsr rsh
##frs: qnr lhk lsr'''

print(solve2(INPUT))

##solve_via_plot(INPUT)
