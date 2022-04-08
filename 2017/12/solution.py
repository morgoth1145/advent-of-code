import lib.aoc
import lib.graph

def parse_graph(s):
    graph = {}

    for line in s.splitlines():
        node, neighbors = line.split(' <-> ')
        graph[int(node)] = list(map(int, neighbors.split(',')))

    return graph

def part1(s):
    graph = lib.graph.to_distance_graph(parse_graph(s))

    answer = 1 + len(list(lib.graph.all_reachable(graph, 0)))

    lib.aoc.give_answer(2017, 12, 1, answer)

def part2(s):
    graph = parse_graph(s)
    unreached = set(graph.keys()) # Extract before converting to a lazy graph

    graph = lib.graph.to_distance_graph(graph)

    answer = 0

    while unreached:
        answer += 1
        start = list(unreached)[0]
        group = lib.graph.all_reachable(graph, start)
        unreached.remove(start)
        unreached -= set(lib.graph.node_dist_list_to_nodes(group))

    lib.aoc.give_answer(2017, 12, 2, answer)

INPUT = lib.aoc.get_input(2017, 12)
part1(INPUT)
part2(INPUT)
