import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    answer = 0

    for c, val in grid.items():
        x, y = c
        if all(grid[n] > val
               for n in grid.neighbors(x, y)):
            answer += val+1

    lib.aoc.give_answer(2021, 9, 1, answer)

def count_basin_size(grid, c):
    basin = {c}
    to_handle = [c]

    while to_handle:
        x, y = to_handle.pop(0)

        for n in grid.neighbors(x, y):
            if n in basin:
                continue
            nval = grid[n]
            if nval != 9:
                basin.add(n)
                to_handle.append(n)

    return len(basin)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    basin_sizes = []

    for c, val in grid.items():
        x, y = c
        if all(grid[n] > val
               for n in grid.neighbors(x, y)):
            basin_sizes.append(count_basin_size(grid, c))

    a, b, c = sorted(basin_sizes)[-3:]
    answer = a*b*c

    lib.aoc.give_answer(2021, 9, 2, answer)

INPUT = lib.aoc.get_input(2021, 9)
part1(INPUT)
part2(INPUT)
