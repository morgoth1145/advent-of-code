import lib.aoc
import lib.graph
import lib.grid

def get_point_of_interest_graph(s):
    grid = lib.grid.FixedGrid.parse(s)

    poi_graph = {}

    for start, v in grid.items():
        if v not in '#.':
            destinations = []

            def neighbor_fn(pos):
                if pos != start and grid[pos] != '.':
                    return
                for n in grid.neighbors(*pos):
                    nv = grid[n]
                    if nv == '#':
                        continue
                    yield n, 1

            for pos, dist in lib.graph.all_reachable(lib.graph.make_lazy_graph(neighbor_fn),
                                                     start):
                if grid[pos] == '.':
                    continue
                destinations.append((int(grid[pos]), dist))

            poi_graph[int(v)] = destinations

    return poi_graph

def solve(s, required_end_node=None):
    poi_graph = get_point_of_interest_graph(s)

    def neighbor_fn(state):
        pos, seen = state
        for neighbor, dist in poi_graph[pos]:
            new_state = (neighbor, tuple(sorted(set(seen + (neighbor,)))))
            yield new_state, dist

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    ALL_POINTS_OF_INTEREST = tuple(sorted(poi_graph.keys()))

    START = (0, (0,))
    END = (0, ALL_POINTS_OF_INTEREST)

    def end_fn(state):
        pos, seen = state
        if required_end_node is not None and required_end_node != pos:
            return False
        return seen == ALL_POINTS_OF_INTEREST

    return lib.graph.dijkstra_length_fuzzy_end(graph, START, end_fn)

def part1(s):
    answer = solve(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 0)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 24)
part1(INPUT)
part2(INPUT)
