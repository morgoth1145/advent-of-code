import collections

import lib.aoc
import lib.graph

def make_grid_neighbor_fn(s):
    n = int(s)
    class LazyGrid(collections.defaultdict):
        def __missing__(self, key):
            x, y = key
            ones = bin(x*x + 3*x + 2*x*y + y + y*y + n).count('1')
            if ones % 2 == 0:
                val = True
            else:
                val = False
            self[key] = val
            return val

    grid = LazyGrid()

    def neighbor_fn(c):
        x, y = c
        if x > 0 and grid[x-1, y]:
            yield (x-1, y), 1
        if y > 0 and grid[x, y-1]:
            yield (x, y-1), 1
        if grid[x+1, y]:
            yield (x+1, y), 1
        if grid[x, y+1]:
            yield (x, y+1), 1

    return neighbor_fn

def part1(s):
    graph = lib.graph.make_lazy_graph(make_grid_neighbor_fn(s))

    answer = lib.graph.dijkstra_length(graph,
                                       (1, 1),
                                       (31, 39))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 13)
part1(INPUT)
part2(INPUT)
