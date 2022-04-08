import functools

import lib.aoc

def solve(serial_number, max_square_size=300):
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            power = rack_id * y
            power += serial_number
            power *= rack_id
            power = (power // 100) % 10
            power -= 5
            grid[x, y] = power

    @functools.cache
    def partial_2d_sum(w, h):
        # AB
        # CD
        # The partial 2D sum to D is the same as the 2D sum to B plus the
        # 2D sum to C minus the 2D sum to A (double-counted) plus cell D
        if w == 1:
            # First column
            if h == 1:
                return grid[1, 1]
            return partial_2d_sum(1, h-1) + grid[1, h]
        if h == 1:
            # First row
            return partial_2d_sum(w-1, 1) + grid[w, 1]

        return (partial_2d_sum(w-1, h) +
                partial_2d_sum(w, h-1) -
                partial_2d_sum(w-1, h-1) +
                grid[w, h])

    def block_power(x, y, w, h):
        # ABC
        # DEF
        # GHI
        # The block sum of E to I is the same as the 2D partial sum to I,
        # minus the double-counting of column A-G and row A-C, plus the
        # block A (because it was double-subtracted)
        power = partial_2d_sum(x+w-1, y+h-1)
        if x > 1:
            power -= partial_2d_sum(x-1, y+h-1)
        if y > 1:
            power -= partial_2d_sum(x+w-1, y-1)
        if x > 1 and y > 1:
            power += partial_2d_sum(x-1, y-1)
        return power

    best_sums = {}

    for square_size in range(1, max_square_size+1):
        best = (-10 * square_size**2, None)

        for x in range(1, 302-square_size):
            for y in range(1, 302-square_size):
                power = block_power(x, y, square_size, square_size)
                best = max(best, (power, (x, y)))

        best_sums[square_size] = best

    return best_sums

def part1(s):
    power, (x, y) = solve(int(s), max_square_size=3)[3]
    answer = f'{x},{y}'

    lib.aoc.give_answer(2018, 11, 1, answer)

def part2(s):
    best_sums = solve(int(s))

    best = (-100, 0, None)

    for square_size, (power, coord) in best_sums.items():
        best = max(best, (power, square_size, coord))

    _, square_size, (x, y) = best

    answer = f'{x},{y},{square_size}'

    lib.aoc.give_answer(2018, 11, 2, answer)

INPUT = lib.aoc.get_input(2018, 11)
part1(INPUT)
part2(INPUT)
