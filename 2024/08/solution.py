import collections

import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    a_to_locs = collections.defaultdict(list)

    for coord, c in grid.items():
        if c != '.':
            a_to_locs[c].append(coord)

    antinodes = set()

    for c, coords in a_to_locs.items():
        for coord_a in coords:
            for coord_b in coords:
                if coord_a == coord_b:
                    continue
                x0, y0 = coord_a
                x1, y1 = coord_b

                dx = x1-x0
                dy = y1-y0

                anti1 = x1+dx, y1+dy
                anti2 = x0-dx, y0-dy

                if anti1 in grid:
                    antinodes.add(anti1)

                if anti2 in grid:
                    antinodes.add(anti2)

    answer = len(antinodes)

    lib.aoc.give_answer(2024, 8, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 8)
part1(INPUT)
part2(INPUT)
