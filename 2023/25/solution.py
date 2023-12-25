import networkx

import lib.aoc

def solve(s):
    g = networkx.Graph()

    for line in s.splitlines():
        src, dests = line.split(': ')
        for d in dests.split():
            g.add_edge(src, d, capacity=1)

    nodes = list(g)

    for idx, n1 in enumerate(nodes):
        for n2 in nodes[idx+1:]:
            num_cuts, (left, right) = networkx.minimum_cut(g, n1, n2)
            if num_cuts == 3:
                return len(left) * len(right)

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2023, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2023, 25)
part1(INPUT)
part2(INPUT)
