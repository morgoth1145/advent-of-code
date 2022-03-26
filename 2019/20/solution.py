import collections
import string

import lib.aoc
import lib.graph
import lib.grid

def parse_maze(s):
    grid = lib.grid.FixedGrid.parse(s)

    points_of_interest = collections.defaultdict(list)

    for (x, y), c in grid.items():
        if c != '.':
            continue

        for n in grid.neighbors(x, y):
            nc = grid[n]
            if len(nc) != 1:
                # Skip any cells we determined were portals!
                continue

            if nc in string.ascii_uppercase:
                dx = n[0] - x
                dy = n[1] - y

                n2 = (x + 2*dx, y + 2*dy)
                nc2 = grid[n2]

                key = nc + nc2
                if dx < 0 or dy < 0:
                    # We read top-down, left-right. This key was read backwards
                    key = key[::-1]

                points_of_interest[key].append((x, y))

                grid[x,y] = key
                grid[n] = '#'
                grid[n2] = ' '

                break

    return grid, points_of_interest

def parse_graph(s):
    grid, points_of_interest = parse_maze(s)

    graph = collections.defaultdict(list)

    for key, locations in points_of_interest.items():
        if len(locations) == 2:
            # Set up the portal
            k1 = key + '1'
            k2 = key + '2'

            loc1, loc2 = locations

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

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 20)
part1(INPUT)
part2(INPUT)
