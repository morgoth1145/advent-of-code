import lib.aoc
import lib.graph

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split(',')
        yield int(a), int(b)

def part1(s):
    data = list(parse_input(s))

    DIMENSION = 70
    NUM_FALL = 1024

    falling_bytes = set(data[:NUM_FALL])

    def neighbor_fn(state):
        x, y = state

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if 0 <= nx <= DIMENSION and 0 <= ny <= DIMENSION:
                if (nx, ny) in falling_bytes:
                    continue # Failed
                yield (nx, ny), 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    start = (0, 0)
    end = (DIMENSION, DIMENSION)

    answer = lib.graph.find_shortest_path_length(graph, start, end)

    lib.aoc.give_answer(2024, 18, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 18)
part1(INPUT)
part2(INPUT)
