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
        n = x+dx, y+dy
        if grid[n] != '#':
            yield (n, (dx, dy)), 1

        yield ((x, y), (-dy, dx)), 1000
        yield ((x, y), (dy, -dx)), 1000

    def end_fn(state):
        return state[0] == end

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    tiles_on_best_path = set()
    num_paths = 0

    minimum_cost = None

    for best_path, path_cost in lib.graph.dijkstra_shortest_paths_fuzzy_end(graph, start_state, end_fn):
        if minimum_cost is None:
            minimum_cost = path_cost
        else:
            assert(minimum_cost == path_cost)

        for coord, direct in best_path:
            tiles_on_best_path.add(coord)

    return minimum_cost, len(tiles_on_best_path)

def part1(s):
    answer, _ = solve(s)

    lib.aoc.give_answer(2024, 16, 1, answer)

def part2(s):
    _, answer = solve(s)

    lib.aoc.give_answer(2024, 16, 2, answer)

INPUT = lib.aoc.get_input(2024, 16)
part1(INPUT)
part2(INPUT)
