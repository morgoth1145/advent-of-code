import lib.aoc
import lib.graph

def parse_graph(s):
    graph = {}

    for line in s.splitlines():
        node, neighbors = line.split(' <-> ')
        node = int(node)
        graph[node] = [(int(neighbor), 1) for neighbor in neighbors.split(',')]

    return graph

def part1(s):
    graph = parse_graph(s)

    answer = 1 + len(list(lib.graph.all_reachable(graph, 0)))

    print(f'The answer to part one is {answer}')

def part2(s):
    graph = parse_graph(s)

    answer = 0
    unreached = set(graph.keys())

    while unreached:
        start = list(unreached)[0]
        group = {start} | {n
                           for n, dist in lib.graph.all_reachable(graph,
                                                                  start)}
        answer += 1
        unreached -= group

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 12)
part1(INPUT)
part2(INPUT)
