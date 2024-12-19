import heapq

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

def part2_bisect(s):
    def predicate(idx):
        return find_num_steps(s, 70, idx+1) == -1

    first_bad_idx = lib.algorithms.bisect(0, len(s.splitlines()), predicate)
    answer = s.splitlines()[first_bad_idx]

    lib.aoc.give_answer(2024, 18, 2, answer)

def part2(s):
    MAX_GRID_COORD = 70

    bad_bytes = list(tuple(map(int, l.split(',')))
                     for l in s.splitlines())
    bad_byte_times = {pos: time
                      for time, pos in enumerate(bad_bytes)}

    grid = {}

    start = (0, 0)
    end = (MAX_GRID_COORD, MAX_GRID_COORD)

    todo = [(-len(bad_bytes), start)]
    grid[start] = len(bad_bytes)

    while todo:
        neg_time, (x, y) = heapq.heappop(todo)
        if (x, y) == end:
            break
        time = -neg_time

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if 0 <= nx <= MAX_GRID_COORD and 0 <= ny <= MAX_GRID_COORD:
                bad_time = bad_byte_times.get((nx, ny), time+1)
                last_good_time = min(time, bad_time-1)

                known_good_time = grid.get((nx, ny))
                if known_good_time is None or known_good_time < last_good_time:
                    grid[nx,ny] = last_good_time
                    heapq.heappush(todo, (-last_good_time, (nx, ny)))

    last_good_idx = grid[end]
    answer = ','.join(map(str, bad_bytes[last_good_idx+1]))

    lib.aoc.give_answer(2024, 18, 2, answer)

INPUT = lib.aoc.get_input(2024, 18)
part1(INPUT)
part2(INPUT)
