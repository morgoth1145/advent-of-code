import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = grid.find('S')
    end = grid.find('E')

    start_state = (start, (1, 0))

    def neighbor_fn(state):
        (x, y), (dx, dy) = state
        n = x+dx, y+dy
        if grid[n] != '#':
            yield (n, (dx, dy)), 1

        yield ((x, y), (-dy, dx)), 1000
        yield ((x, y), (dy, -dx)), 1000

    def end_fn(state):
        return state[0] == end

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = lib.graph.dijkstra_length_fuzzy_end(graph, start_state, end_fn)

    lib.aoc.give_answer(2024, 16, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 16)
part1(INPUT)
part2(INPUT)
