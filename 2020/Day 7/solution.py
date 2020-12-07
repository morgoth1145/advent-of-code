import collections

import helpers.input

def parse_bags(s):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        outer, inner = line.split('bags contain')
        outer = outer.strip()
        inner = inner.strip()
        stuff = inner.split(',')
        for item in stuff:
            amount, item = item.split(maxsplit=1)
            while item[-1] in '.s':
                item = item[:-1]
            assert(item.endswith('bag'))
            item = item[:-3].strip()
            graph[outer].append((item, amount))
    return graph

def can_contain(graph, key, inner):
    for item, amount in graph.get(key, []):
        if item == inner:
            return True
        if can_contain(graph, item, inner):
            return True
    return False

def part1(s):
    graph = parse_bags(s)
    answer = sum(1 for key in graph.keys() if can_contain(graph, key, 'shiny gold'))
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 7)

part1(INPUT)
part2(INPUT)
