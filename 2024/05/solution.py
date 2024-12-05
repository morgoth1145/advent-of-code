import collections

import lib.aoc
import lib.graph

def parse_input(s):
    a, b = s.split('\n\n')

    rules = collections.defaultdict(set)
    for l in a.split('\n'):
        first, second = tuple(map(int, l.split('|')))
        rules[first].add(second)

    blist = []
    for l in b.split('\n'):
        blist.append(tuple(map(int, l.split(','))))

    return rules, blist

def verify(rules, l):
    previous = set()

    for item in l:
        if len(previous & rules[item]) > 0:
            return False
        previous.add(item)

    return True

def part1(s):
    rules, b = parse_input(s)

    answer = sum(l[len(l)//2]
                 for l in b
                 if verify(rules, l))

    lib.aoc.give_answer(2024, 5, 1, answer)

def reorder(rules, l):
    # Extract the "mini" graph for this line as the larger rule graph is cyclic
    # and cannot be topo-sorted
    all_items = set(l)

    mini_graph = {
        item: rules[item] & all_items
        for item in l
    }

    return lib.graph.topological_sort_root_first(mini_graph)

def part2(s):
    rules, b = parse_input(s)

    answer = 0

    for l in b:
        if not verify(rules, l):
            l = reorder(rules, l)
            assert(verify(rules, l))
            answer += l[len(l)//2]

    lib.aoc.give_answer(2024, 5, 2, answer)

INPUT = lib.aoc.get_input(2024, 5)
part1(INPUT)
part2(INPUT)
