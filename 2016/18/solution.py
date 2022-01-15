import gmpy2

import lib.aoc

def solve(s, total_rows):
    row = 0
    mask = 0

    # Convert the row into a binary number with 1's marking traps
    for c in s:
        row <<= 1
        mask <<= 1
        mask += 1
        if c == '^':
            row += 1

    # Count trap tile bits
    # TODO: Maybe row.bit_count() with Python 3.10?
    trap_tiles = gmpy2.popcount(row)

    for _ in range(total_rows-1):
        # Each iteration only cares about how the left and right sides interact
        # A tile is a trap iff the previous left and right tiles are opposites
        # Since safe tiles are 0, this is a simple XOR operation on shifted
        # rows, with a mask to limit the width of the rows
        left = row >> 1
        right = row << 1
        row = (left ^ right) & mask

        trap_tiles += gmpy2.popcount(row)

    # We care about safe tiles :)
    return len(s) * total_rows - trap_tiles

def part1(s):
    answer = solve(s, 40)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 400000)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 18)
part1(INPUT)
part2(INPUT)
