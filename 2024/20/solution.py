import numpy

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

    def make_dist_arr(start):
        # Default everywhere to a large value to "poison" walls
        arr = numpy.zeros((grid.width, grid.height)) + len(s)

        for pos, time in lib.graph.all_reachable(graph, start):
            arr[pos] = time
        arr[start] = 0 # Not included in all_reachable

        return arr

    start = grid.find('S')
    end = grid.find('E')

    a_start = make_dist_arr(start)
    a_end = make_dist_arr(end)

    normal_time = a_start[end]

    def cheat_slices(delta, size):
        if delta > 0:
            return slice(delta, size), slice(0, size-delta)
        else:
            return slice(0, size+delta), slice(-delta, size)

    def cheat(dx, dy):
        extra_time = abs(dx) + abs(dy)

        start_x_slice, end_x_slice = cheat_slices(dx, grid.width)
        start_y_slice, end_y_slice = cheat_slices(dy, grid.height)

        return (a_start[start_x_slice, start_y_slice] +
                a_end[end_x_slice, end_y_slice] +
                extra_time)

    answer = 0

    for dx in range(-max_cheat_time, max_cheat_time+1):
        if abs(dx) >= grid.width:
            # In case of absurd cheat times, make sure the slicing is sane!
            continue
        rem_cheat = max_cheat_time - abs(dx)
        for dy in range(-rem_cheat, rem_cheat+1):
            if abs(dy) >= grid.height:
                # In case of absurd cheat times, make sure the slicing is sane!
                continue
            savings = normal_time - cheat(dx, dy)

            answer += numpy.count_nonzero(savings >= minimum_savings)

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
