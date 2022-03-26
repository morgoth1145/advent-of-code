import string

import lib.aoc
import lib.graph
import lib.grid

def find_points_of_interest(grid):
    keys = {}
    doors = {}
    start = None

    for coord, c in grid.items():
        if c in '.#':
            continue
        if c == '@':
            assert(start is None)
            start = coord
            continue
        if c in string.ascii_lowercase:
            assert(c not in keys)
            keys[c] = coord
            continue
        if c in string.ascii_uppercase:
            assert(c not in doors)
            doors[c] = coord
            continue
        assert(False)

    return keys, doors, start

def make_connectivity_graph(grid, points_of_interest):
    connectivity_graph = {}

    for start_symbol, start_coord in points_of_interest.items():
        def grid_neighbor_fn(coord):
            if grid[coord] not in ('.', start_symbol):
                # Don't traverse past any point of interest
                return

            for n in grid.neighbors(*coord):
                c = grid[n]
                if c == '#':
                    continue

                yield n, 1

        grid_graph = lib.graph.make_lazy_graph(grid_neighbor_fn)

        reachable = []
        for coord, dist in lib.graph.all_reachable(grid_graph, start_coord):
            c = grid[coord]
            if c in '.#':
                continue
            assert(c != start_symbol)
            reachable.append((c, dist))

        connectivity_graph[start_symbol] = reachable

    return connectivity_graph

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    keys, doors, start = find_points_of_interest(grid)

    connectivity_graph = make_connectivity_graph(grid,
                                                 keys | doors | {'@': start})

    def neighbor_fn(state):
        symbol, keys = state

        for neighbor, dist in connectivity_graph[symbol]:
            if neighbor in string.ascii_lowercase:
                new_keys = tuple(sorted(set(keys + (neighbor,))))
                yield (neighbor, new_keys), dist
                continue
            if neighbor in string.ascii_uppercase:
                if neighbor.swapcase() not in keys:
                    # Can't cross this door yet
                    continue
            yield (neighbor, keys), dist

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    ALL_KEYS = tuple(sorted(keys.keys()))

    def have_all_keys(state):
        symbol, keys = state
        return keys == ALL_KEYS

    answer = lib.graph.dijkstra_length_fuzzy_end(graph,
                                                 ('@', tuple()),
                                                 have_all_keys)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 18)
part1(INPUT)
part2(INPUT)
