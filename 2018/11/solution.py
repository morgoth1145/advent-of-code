import lib.aoc

def make_grid(serial_number):
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            power = rack_id * y
            power += serial_number
            power *= rack_id
            power = (power // 100) % 10
            power -= 5
            grid[x,y] = power

    return grid

def optimize(grid, square_size):
    presums = {}

    for y in range(1, 301):
        power = 0
        for x in range(1, square_size):
            power += grid[x,y]

        for x in range(1, 302 - square_size):
            power += grid[x+square_size-1,y]
            presums[x,y] = power
            power -= grid[x,y]

    best = (0, (0, 0))

    for x in range(1, 302 - square_size):
        power = 0
        for y in range(1, square_size):
            power += presums[x,y]

        for y in range(1, 302 - square_size):
            power += presums[x,y+square_size-1]
            best = max(best, (power, (x, y)))
            power -= presums[x,y]

    return best

def part1(s):
    grid = make_grid(int(s))

    best = optimize(grid, 3)

    best_x, best_y = best[1]
    answer = f'{best_x},{best_y}'

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = make_grid(int(s))

    best = (-100, 0, None)

    for square_size in range(1, 301):
        power, coord = optimize(grid, square_size)
        best = max(best, (power, square_size, coord))

    _, square_size, (x, y) = best

    answer = f'{x},{y},{square_size}'

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 11)
part1(INPUT)
part2(INPUT)
