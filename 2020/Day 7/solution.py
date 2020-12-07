import collections

import helpers.graph
import helpers.input

def parse_bags(s):
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        outer, inner = line.split('bags contain')
        outer = outer.strip()
        inner = inner.strip()
        if inner == 'no other bags.':
            # This bag is empty
            continue
        stuff = inner.split(',')
        for item in stuff:
            amount, item = item.split(maxsplit=1)
            while item[-1] in '.s':
                item = item[:-1]
            assert(item.endswith('bag'))
            item = item[:-3].strip()
            graph[outer].append((item, int(amount)))
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

def custom_topo_sort_thing(bag_graph):
    graph = {}
    for key, items in bag_graph.items():
        graph[key] = [t for t,_ in items]
    return helpers.graph.topological_sort(graph)

def part2(s):
    graph = parse_bags(s)
    leaf_to_root = list(custom_topo_sort_thing(graph))
    bag_content_counts = {}
    for bag in leaf_to_root:
        total = sum(n * (1 + bag_content_counts.get(t,0)) for t,n in graph[bag])
        bag_content_counts[bag] = total
    answer = bag_content_counts['shiny gold']
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 7)

part1(INPUT)
part2(INPUT)
