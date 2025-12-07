import functools

import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    split_points = set()

    @functools.cache
    def run_splits(x, y):
        while y < grid.height:
            c = grid[x,y]
            if c == '^':
                split_points.add((x, y))
                run_splits(x-1, y)
                run_splits(x+1, y)
                return
            y += 1
        return

    x, y = grid.find('S')
    run_splits(x, y)

    answer = len(split_points)

    lib.aoc.give_answer(2025, 7, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 7)
part1(INPUT)
part2(INPUT)
