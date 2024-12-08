import collections

import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = sum(1
                 for coord, direct
                 in grid.find_matches('XMAS',
                                      include_diagonals=True,
                                      allow_reverse=True))

    lib.aoc.give_answer(2024, 4, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    # Count how many times each A is part of a 'MAS' diagonal
    # If it is part of 2 'MAS' diagonals then it is an X-MAS!
    a_match_counts = collections.Counter()
    for (x, y), (dx, dy) in grid.find_matches('MAS',
                                              include_orthogonals=False,
                                              include_diagonals=True,
                                              allow_reverse=True):
        a_match_counts[x+dx, y+dy] += 1

    answer = sum(1
                 for v in a_match_counts.values()
                 if v == 2)

    lib.aoc.give_answer(2024, 4, 2, answer)

INPUT = lib.aoc.get_input(2024, 4)
part1(INPUT)
part2(INPUT)
