import collections
import string

import lib.aoc
import lib.graph
import lib.grid

def parse_maze(s):
    grid = lib.grid.FixedGrid.parse(s)

    points_of_interest = collections.defaultdict(list)

    for (x, y), c in grid.items():
        if c in string.ascii_uppercase:
            # Read in top-down, left-right fashion
            for dx, dy in [(1, 0),
                           (0, 1)]:
                if (x+dx, y+dy) not in grid:
                    continue

                nc = grid[x+dx, y+dy]
                if nc not in string.ascii_uppercase:
                    continue

                key = c+nc

                if (x-dx, y-dy) in grid and grid[x-dx, y-dy] == '.':
                    loc = (x-dx, y-dy)
                else:
                    loc = (x+2*dx, y+2*dy)
                    assert(grid[loc] == '.')

                points_of_interest[key].append(loc)
                grid[loc] = key
                grid[x,y] = '#'
                grid[x+dx, y+dy] = '#'
                break

    return grid, points_of_interest

def parse_graph(s):
    grid, points_of_interest = parse_maze(s)

    OUTER_X = (2, grid.width-3)
    OUTER_Y = (2, grid.height-3)

    graph = collections.defaultdict(list)

    for key, locations in points_of_interest.items():
        if len(locations) == 2:
            # Set up the portal
            loc1, loc2 = locations

            if loc1[0] in OUTER_X or loc1[1] in OUTER_Y:
                k1 = key + '_OUT'
                k2 = key + '_IN'
            else:
                assert(loc2[0] in OUTER_X or loc2[1] in OUTER_Y)
                k1 = key + '_IN'
                k2 = key + '_OUT'

            grid[loc1] = k1
            grid[loc2] = k2

            graph[k1].append((k2, 1))
            graph[k2].append((k1, 1))
        else:
            assert(len(locations) == 1)

    def grid_neighbor_fn(coord):
        x, y = coord

        for n in grid.neighbors(x, y):
            nc = grid[n]

            if nc == '#':
                # Wall
                continue

            assert(nc != ' ')
            yield n, 1

    grid_graph = lib.graph.make_lazy_graph(grid_neighbor_fn)

    for locations in points_of_interest.values():
        for loc in locations:
            key = grid[loc]

            for dest, dist in lib.graph.all_reachable(grid_graph, loc):
                dest_key = grid[dest]
                if dest_key != '.':
                    # Named location
                    graph[key].append((dest_key, dist))

    return graph

def part1(s):
    graph = parse_graph(s)

    answer = lib.graph.dijkstra_length(graph, 'AA', 'ZZ')

    lib.aoc.give_answer(2019, 20, 1, answer)

def part2(s):
    base_graph = parse_graph(s)

    def recursive_neighbor_fn(state):
        key, level = state

        for dest_key, dist in base_graph[key]:
            if level > 0 and dest_key in ('AA', 'ZZ'):
                # Walls
                continue

            if dest_key[:2] == key[:2]:
                # Portal, this affects our level!
                if key.endswith('_IN'):
                    yield (dest_key, level+1), dist
                else:
                    assert(key.endswith('_OUT'))
                    yield (dest_key, level-1), dist
                continue

            if level == 0 and dest_key.endswith('_OUT'):
                # Walls
                continue

            # Staying on the same level
            yield (dest_key, level), dist

    graph = lib.graph.make_lazy_graph(recursive_neighbor_fn)

    answer = lib.graph.dijkstra_length(graph, ('AA', 0), ('ZZ', 0))

    lib.aoc.give_answer(2019, 20, 2, answer)

INPUT = lib.aoc.get_input(2019, 20)
part1(INPUT)
part2(INPUT)
