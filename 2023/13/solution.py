from itertools import starmap
import operator

import lib.aoc
import lib.grid

def score_reflection(grid, smudges=0):
    right = list(map(''.join, map(grid.col, grid.x_range)))
    left = []
    while len(right) > 1:
        left.insert(0, right.pop(0))
        num_diffs = sum(starmap(operator.ne,
                                zip(''.join(left),
                                    ''.join(right))))
        if num_diffs == smudges:
            return len(left)

    bottom = list(map(''.join, map(grid.row, grid.y_range)))
    top = []
    while len(bottom) > 1:
        top.insert(0, bottom.pop(0))
        num_diffs = sum(starmap(operator.ne,
                                zip(''.join(top),
                                    ''.join(bottom))))
        if num_diffs == smudges:
            return len(top) * 100

def solve(s, smudges=0):
    return sum(score_reflection(g, smudges)
               for g in map(lib.grid.FixedGrid.parse,
                            s.split('\n\n')))

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2023, 13, 1, answer)

def part2(s):
    answer = solve(s, smudges=1)

    lib.aoc.give_answer(2023, 13, 2, answer)

INPUT = lib.aoc.get_input(2023, 13)
part1(INPUT)
part2(INPUT)
