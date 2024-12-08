import collections
import math

import lib.aoc
import lib.grid

def solve(s, generate_antinodes):
    grid = lib.grid.FixedGrid.parse(s)

    frequency_to_antennas = collections.defaultdict(list)

    for coord, c in grid.items():
        if c != '.':
            frequency_to_antennas[c].append(coord)

    antinodes = set()

    for c, coords in frequency_to_antennas.items():
        for coord_a in coords:
            for coord_b in coords:
                if coord_a == coord_b:
                    continue
                x0, y0 = coord_a
                x1, y1 = coord_b

                dx = x1-x0
                dy = y1-y0

                for antinode in generate_antinodes(grid, x0, y0, dx, dy):
                    if antinode in grid:
                        antinodes.add(antinode)

    return len(antinodes)

def part1(s):
    def generate_antinodes(grid, x0, y0, dx, dy):
        yield x0-dx, y0-dy
        yield x0+2*dx, y0+2*dy

    answer = solve(s, generate_antinodes)

    lib.aoc.give_answer(2024, 8, 1, answer)

def part2(s):
    def generate_antinodes(grid, x0, y0, dx, dy):
        x, y = x0, y0

        # Scale the slope to capture everything!
        slope_mult = math.gcd(dx, dy)
        dx //= slope_mult
        dy //= slope_mult

        # Start at one side of the grid and generate to the other side of the grid
        while (x-dx, y-dy) in grid:
            x, y = x-dx, y-dy
        while (x, y) in grid:
            yield x, y
            x, y = x+dx, y+dy

    answer = solve(s, generate_antinodes)

    lib.aoc.give_answer(2024, 8, 2, answer)

INPUT = lib.aoc.get_input(2024, 8)
part1(INPUT)
part2(INPUT)
