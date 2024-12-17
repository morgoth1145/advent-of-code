import lib.aoc
import lib.graph
import lib.grid

def solve(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = grid.find('S')
    end = grid.find('E')

    start_state = (start, (1, 0))

    def neighbor_fn(state):
        (x, y), (dx, dy) = state

        # Always move even if a turn is required
        # This helps keep the state space down and the graph smaller,
        # optimizing the solution
        for ndx, ndy, cost in [(dx, dy, 1),
                               (-dy, dx, 1001),
                               (dy, -dx, 1001),
                               (-dy, -dx, 2001)]:
            n = x+ndx, y+ndy
            if grid[n] != '#':
                yield (n, (ndx, ndy)), cost

    def end_fn(state):
        return state[0] == end

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    shortest_path_graph, _, minimum_cost, _ = lib.graph.make_shortest_path_graph_fuzzy_end(graph, start_state, end_fn)

    # Eliminate duplicates in case some tiles are hit from multiple directions
    tiles_on_shortest_path = set(pos
                                 for pos, direct
                                 in shortest_path_graph.keys())

    return minimum_cost, len(tiles_on_shortest_path)

def part1(s):
    answer, _ = solve(s)

    lib.aoc.give_answer(2024, 16, 1, answer)

def part2(s):
    _, answer = solve(s)

    lib.aoc.give_answer(2024, 16, 2, answer)

INPUT = lib.aoc.get_input(2024, 16)
part1(INPUT)
part2(INPUT)
