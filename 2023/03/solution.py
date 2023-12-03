import collections
import math

import lib.aoc
import lib.grid

def parse_schematic(s):
    grid = lib.grid.FixedGrid.parse(s)

    symbol_positions = collections.defaultdict(set)
    numbers = []

    for y in range(grid.height):
        num = None
        num_start_x = None

        def handle_num(end_x):
            nonlocal num, num_start_x

            num = int(num)

            border = {(num_start_x-1, y),
                      (end_x, y)}
            for check_x in range(num_start_x-1, end_x+1):
                border.add((check_x, y-1))
                border.add((check_x, y+1))

            numbers.append((int(num), border))

            num = None
            num_start_x = None

        for x in range(grid.width):
            c = grid[x,y]
            if c.isdigit():
                if num is None:
                    num = c
                    num_start_x = x
                else:
                    num += c
            else:
                if num is not None:
                    # x is one past the number's end
                    handle_num(x)
                if c != '.':
                    symbol_positions[c].add((x, y))

        if num is not None:
            handle_num(grid.width)

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
