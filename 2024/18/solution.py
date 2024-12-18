import lib.algorithms
import lib.aoc
import lib.graph

def find_num_steps(s, max_grid_coord, num_fallen_bytes):
    bad_bytes = set(tuple(map(int, l.split(',')))
                    for l in s.splitlines()[:num_fallen_bytes])

    def neighbor_fn(pos):
        x, y = pos

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if 0 <= nx <= max_grid_coord and 0 <= ny <= max_grid_coord:
                if (nx, ny) in bad_bytes:
                    continue # Failed
                yield (nx, ny), 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    start = (0, 0)
    end = (max_grid_coord, max_grid_coord)

    return lib.graph.find_shortest_path_length(graph, start, end)

def part1(s):
    answer = find_num_steps(s, 70, 1024)

    lib.aoc.give_answer(2024, 18, 1, answer)

def part2(s):
    def predicate(idx):
        return find_num_steps(s, 70, idx+1) == -1

    first_bad_idx = lib.algorithms.bisect(0, len(s.splitlines()), predicate)
    answer = s.splitlines()[first_bad_idx]

    lib.aoc.give_answer(2024, 18, 2, answer)

INPUT = lib.aoc.get_input(2024, 18)
part1(INPUT)
part2(INPUT)
