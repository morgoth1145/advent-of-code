import lib.aoc
import lib.graph
import lib.grid

def solve(s, max_cheat_time, minimum_savings):
    grid = lib.grid.FixedGrid.parse(s)

    def neighbor_fn(pos):
        for n in grid.neighbors(*pos):
            if grid[n] == '#':
                continue

            yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def precompute_distances(start):
        distances = dict(lib.graph.all_reachable(graph, start))
        distances[start] = 0
        return distances

    start = grid.find('S')

    cheat_starts = precompute_distances(start)
    remaining_time = precompute_distances(grid.find('E'))

    normal_time = remaining_time[start]

    answer = 0

    def cheat(pos):
        x, y = pos
        for end_y in range(max(0, y-max_cheat_time),
                           min(y+max_cheat_time+1, grid.height)):
            y_dist = abs(y-end_y)
            rem_dist = max_cheat_time - y_dist
            for end_x in range(max(0, x-rem_dist),
                               min(x+rem_dist+1, grid.height)):
                end_time = remaining_time.get((end_x, end_y))
                if end_time is None:
                    continue

                yield abs(x-end_x) + y_dist + end_time

    for cheat_start, time in cheat_starts.items():
        for cheat_time in cheat(cheat_start):
            total_time = time + cheat_time

            if normal_time - total_time >= minimum_savings:
                answer += 1

    return answer

def part1(s):
    answer = solve(s, 2, 100)

    lib.aoc.give_answer(2024, 20, 1, answer)

def part2(s):
    answer = solve(s, 20, 100)

    lib.aoc.give_answer(2024, 20, 2, answer)

INPUT = lib.aoc.get_input(2024, 20)
part1(INPUT)
part2(INPUT)
