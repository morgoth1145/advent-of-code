import re

import helpers.input

def parse_bags(s):
    graph = {}
    for line in s.splitlines():
        outer, inner = line.split('bags contain')
        outer = outer.strip()
        contents = []
        for amount, item in re.findall('(\d+) ([\w ]+) bag', inner):
            contents.append((item, int(amount)))
        graph[outer] = contents
    return graph

def can_contain(graph, key, inner):
    for item, amount in graph.get(key, []):
        if item == inner or can_contain(graph, item, inner):
            return True
    return False

def part1(s):
    graph = parse_bags(s)
    answer = sum(1
                 for key
                 in graph.keys()
                 if can_contain(graph, key, 'shiny gold'))
    print(f'The answer to part one is {answer}')

def count_contents(graph, bag):
    return sum(n * (1 + count_contents(graph, t))
               for t,n
               in graph[bag])

def part2(s):
    graph = parse_bags(s)
    answer = count_contents(graph, 'shiny gold')
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 7)

part1(INPUT)
part2(INPUT)
