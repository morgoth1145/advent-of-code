import lib.aoc
import lib.graph
import lib.lazy_dict

def parse_graph(s):
    n = int(s)

    def grid_cell_fn(coord):
        x, y = coord
        ones = bin(x*x + 3*x + 2*x*y + y + y*y + n).count('1')
        return ones % 2 == 0

    grid = lib.lazy_dict.make_lazy_dict(grid_cell_fn)

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

    return lib.graph.make_lazy_graph(neighbor_fn)

def part1(s):
    graph = parse_graph(s)

    answer = lib.graph.dijkstra_length(graph,
                                       (1, 1),
                                       (31, 39))

    lib.aoc.give_answer(2016, 13, 1, answer)

def part2(s):
    graph = parse_graph(s)

    answer = len(list(lib.graph.all_reachable(graph, (1, 1), 50)))
    answer += 1 # all_reachable excludes the start location

    lib.aoc.give_answer(2016, 13, 2, answer)

INPUT = lib.aoc.get_input(2016, 13)
part1(INPUT)
part2(INPUT)
