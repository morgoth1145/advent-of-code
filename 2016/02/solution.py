import string

import lib.aoc

def map_key(directions):
    x, y = 1, 1

    for d in directions:
        if d == 'U':
            y = max(y-1, 0)
        elif d == 'D':
            y = min(y+1, 2)
        elif d == 'L':
            x = max(x-1, 0)
        elif d == 'R':
            x = min(x+1, 2)

    return str(3*y + x + 1)

def part1(s):
    answer = int(''.join(map(map_key, s.splitlines())))

    lib.aoc.give_answer(2016, 2, 1, answer)

KEYLIST = string.digits + string.ascii_uppercase

def map_diamond_key(directions):
    x, y = -2, 0 # Start on 5

    for d in directions:
        if d == 'U':
            nx, ny = x, y-1
        elif d == 'D':
            nx, ny = x, y+1
        elif d == 'L':
            nx, ny = x-1, y
        elif d == 'R':
            nx, ny = x+1, y

        if abs(nx) + abs(ny) <= 2:
            x, y = nx, ny

    offset = 1
    for skipped_y in range(-2, y):
        num_in_row = 2 * (2 - abs(skipped_y)) + 1
        offset += num_in_row

    max_x_for_row = (2 - abs(y))
    offset += x + max_x_for_row

    return KEYLIST[offset]

def part2(s):
    answer = ''.join(map(map_diamond_key, s.splitlines()))

    lib.aoc.give_answer(2016, 2, 2, answer)

INPUT = lib.aoc.get_input(2016, 2)
part1(INPUT)
part2(INPUT)
