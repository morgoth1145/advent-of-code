import lib.algorithms
import lib.aoc
import lib.graph

import lib.performance

def parse_falling_bytes(s):
    return (tuple(map(int, l.split(',')))
            for l in s.splitlines())

@lib.performance.timed
def part1(s):
    MAX_GRID_COORD = 70
    NUM_FALLEN_BYTES = 1024

    bad_bytes = set(list(parse_falling_bytes(s))[:NUM_FALLEN_BYTES])

    def neighbor_fn(pos):
        x, y = pos

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if 0 <= nx <= MAX_GRID_COORD and 0 <= ny <= MAX_GRID_COORD:
                if (nx, ny) in bad_bytes:
                    continue # Failed
                yield (nx, ny), 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    start = (0, 0)
    end = (MAX_GRID_COORD, MAX_GRID_COORD)

    answer = lib.graph.find_shortest_path_length(graph, start, end)

    lib.aoc.give_answer(2024, 18, 1, answer)

@lib.performance.timed
def part2(s):
    falling_bytes = list(parse_falling_bytes(s))

    MAX_GRID_COORD = 70

    grid = {(x,y): set([(x,y)])
            for x in range(MAX_GRID_COORD+1)
            for y in range(MAX_GRID_COORD+1)}

    # Block all the falling bytes!
    for x, y in falling_bytes:
        grid[x,y] = None

    def perform_union(x, y):
        self_set = grid[x,y]
        for n in [(x-1, y),
                  (x+1, y),
                  (x, y-1),
                  (x, y+1)]:
            other_set = grid.get(n)
            if other_set is None:
                continue
            # Merge and update references
            if len(self_set) > len(other_set):
                # Make sure to propagate to the smaller set for speed
                self_set, other_set = other_set, self_set
            other_set.update(self_set)
            for pos in self_set:
                grid[pos] = other_set
            self_set = other_set

        return self_set

    for pos, group in grid.items():
        if group is not None:
            perform_union(*pos)

    start = (0, 0)
    end = (MAX_GRID_COORD, MAX_GRID_COORD)

    assert(end not in grid[start])

    for pos in falling_bytes[::-1]:
        grid[pos] = set([pos])
        union_group = perform_union(*pos)

        if start in union_group and end in union_group:
            # This was the position that bocked the path!
            answer = ','.join(map(str, pos))
            break

    print(len(falling_bytes), falling_bytes.index(pos))

    lib.aoc.give_answer(2024, 18, 2, answer)

INPUT = lib.aoc.get_input(2024, 18)
part1(INPUT)
part2(INPUT)
