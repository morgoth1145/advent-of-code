import lib.aoc
import lib.graph
import lib.grid

def parse_graph_for_reverse_search(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = None
    end = None

    for c, val in grid.items():
        if val == 'S':
            grid[c] = 'a'
            start = c
        elif val == 'E':
            grid[c] = 'z'
            end = c

    def neighbor_fn(pos):
        self = grid[pos]
        for n in grid.neighbors(*pos):
            if ord(grid[n]) - ord(self) <= 1:
                yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    return grid, graph, start, end

def part1(s):
    _, graph, start, end = parse_graph_for_reverse_search(s)
    answer = lib.graph.dijkstra_length(graph, start, end)
    lib.aoc.give_answer(2022, 12, 1, answer)

def part2(s):
    grid, graph, start, end = parse_graph_for_reverse_search(s)
    start = [c for c,val in grid.items() if val == 'a']
    answer = lib.graph.dijkstra_length(graph, start, end)
    lib.aoc.give_answer(2022, 12, 2, answer)

INPUT = lib.aoc.get_input(2022, 12)
part1(INPUT)
part2(INPUT)
