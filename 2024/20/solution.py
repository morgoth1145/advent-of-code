import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = grid.find('S')
    end = grid.find('E')

    def neighbor_fn(pos):
        for n in grid.neighbors(*pos):
            nv = grid[n]

            if nv == '#':
                continue

            yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    normal_time = lib.graph.find_shortest_path_length(graph, start, end)

    answer = 0

    def cheat_options(pos):
        cands = set()
        for n in grid.neighbors(*pos):
            cands.update(grid.neighbors(*n))

        for n2 in cands:
            if n2 == pos or grid[n2] == '#':
                continue
            yield n2

    remaining_time = {}
    remaining_time[end] = 0

    for pos, dist in lib.graph.all_reachable(graph, end):
        remaining_time[pos] = dist

    assert(end in remaining_time)

    cheat_starts = {}
    cheat_starts[start] = 0

    for pos, dist in lib.graph.all_reachable(graph, start):
        cheat_starts[pos] = dist

    assert(start in cheat_starts)

    for cheat_start, dist in cheat_starts.items():
        for cheat_next in cheat_options(cheat_start):
            sub_dist = remaining_time.get(cheat_next)

            total_dist = dist + 2 + sub_dist

            savings = normal_time - total_dist

            if savings <= 0:
                continue

            if total_dist + 100 <= normal_time:
                assert(savings >= 100)
                answer += 1
            else:
                assert(savings < 100)

    lib.aoc.give_answer(2024, 20, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = grid.find('S')
    end = grid.find('E')

    def neighbor_fn(pos):
        for n in grid.neighbors(*pos):
            nv = grid[n]

            if nv == '#':
                continue

            yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    normal_time = lib.graph.find_shortest_path_length(graph, start, end)

    answer = 0

    def cheat_options(pos):
        cheat_ends = {}
        all_cands = set()
        cands = set()
        cands.add(pos)
        for time in range(20):
            new_cands = set()
            for p in cands:
                cheat_ends[p] = time
                new_cands.update(grid.neighbors(*p))
            cands = new_cands - all_cands
            all_cands.update(cands)
        for p in cands:
            cheat_ends[p] = 20
        return cheat_ends.items()

    remaining_time = {}
    remaining_time[end] = 0

    for pos, dist in lib.graph.all_reachable(graph, end):
        remaining_time[pos] = dist

    assert(end in remaining_time)

    cheat_starts = {}
    cheat_starts[start] = 0

    for pos, dist in lib.graph.all_reachable(graph, start):
        cheat_starts[pos] = dist

    assert(start in cheat_starts)

    for cheat_start, dist in cheat_starts.items():
        for cheat_next, cheat_time in cheat_options(cheat_start):
            sub_dist = remaining_time.get(cheat_next)
            if sub_dist is None:
                continue

            total_dist = dist + cheat_time + sub_dist

            savings = normal_time - total_dist

            if savings <= 0:
                continue

            if total_dist + 100 <= normal_time:
                assert(savings >= 100)
                answer += 1
            else:
                assert(savings < 100)

    lib.aoc.give_answer(2024, 20, 2, answer)

INPUT = lib.aoc.get_input(2024, 20)
part1(INPUT)
part2(INPUT)
