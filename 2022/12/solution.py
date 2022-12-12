import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = None
    end = None

    for c, val in grid.items():
        if val == 'S':
            start = c
        elif val == 'E':
            end = c

    def neighbor_fn(pos):
        self = grid[pos]
        for n in grid.neighbors(*pos):
            val = grid[n]
            if self == 'S':
                if val in 'ab':
                    yield n, 1
            elif val == 'E':
                if self in 'yz':
                    yield n, 1
            elif ord(val) - ord(self) <= 1:
                yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = lib.graph.dijkstra_length(graph, start, end)

    lib.aoc.give_answer(2022, 12, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    starts = []
    end = None

    for c, val in grid.items():
        if val in 'Sa':
            starts.append(c)
        elif val == 'E':
            end = c

    def neighbor_fn(pos):
        self = grid[pos]
        for n in grid.neighbors(*pos):
            val = grid[n]
            if self == 'S':
                if val in 'ab':
                    yield n, 1
            elif val == 'E':
                if self in 'yz':
                    yield n, 1
            elif ord(val) - ord(self) <= 1:
                yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = None
    for start in starts:
        cand = lib.graph.dijkstra_length(graph, start, end)
        if cand != -1:
            if answer is None or answer > cand:
                answer = cand

    lib.aoc.give_answer(2022, 12, 2, answer)

INPUT = lib.aoc.get_input(2022, 12)
part1(INPUT)
part2(INPUT)
