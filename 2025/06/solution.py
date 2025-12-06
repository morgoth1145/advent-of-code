import math

import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s,
                                    linesplit_fn=lambda line: line.split(),
                                    value_fn=str)

    answer = 0

    for x in grid.x_range:
        col = grid.col(x)

        op = col[-1]

        nums = list(map(int, col[:-1]))

        if op == '+':
            answer += sum(nums)
        elif op == '*':
            answer += math.prod(nums)
        else:
            assert(False)

    lib.aoc.give_answer(2025, 6, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 6)
part1(INPUT)
part2(INPUT)
