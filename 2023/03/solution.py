import collections
import math

import lib.aoc
import lib.grid

def parse_schematic(s):
    grid = lib.grid.FixedGrid.parse(s)

    symbol_positions = collections.defaultdict(set)
    numbers = []

    for y in range(grid.height):
        num = 0
        num_border = set()

        for x in range(grid.width):
            c = grid[x,y]
            if c.isdigit():
                if num == 0:
                    # Start of number, get the border on the left
                    num_border |= {(x-1, y-1), (x-1, y), (x-1, y+1)}

                num = 10 * num + int(c)
                num_border |= {(x, y-1), (x, y+1)}
            else:
                if num > 0:
                    # Add the border on the right
                    num_border |= {(x, y-1), (x, y), (x, y+1)}
                    numbers.append((num, num_border))
                    num = 0
                    num_border = set()
                if c != '.':
                    symbol_positions[c].add((x, y))

        if num > 0:
            num_border |= {(grid.width, y-1), (grid.width, y), (grid.width, y+1)}
            numbers.append((num, num_border))

    return symbol_positions, numbers

def part1(s):
    symbol_positions, numbers = parse_schematic(s)

    symbols = set()
    for places in symbol_positions.values():
        symbols |= places

    answer = sum(n for n, border in numbers
                 if len(border & symbols) > 0)

    lib.aoc.give_answer(2023, 3, 1, answer)

def part2(s):
    symbol_positions, numbers = parse_schematic(s)

    gears = collections.defaultdict(list)

    for n, border in numbers:
        for coord in border & symbol_positions['*']:
            gears[coord].append(n)

    answer = sum(math.prod(gear_nums)
                 for gear_nums in gears.values()
                 if len(gear_nums) == 2)

    lib.aoc.give_answer(2023, 3, 2, answer)

INPUT = lib.aoc.get_input(2023, 3)

part1(INPUT)
part2(INPUT)
