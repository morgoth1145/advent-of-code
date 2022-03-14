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

def part1(s):
    grid = make_grid(int(s))

    best = (0, (0, 0))

    for x, y in grid:
        tot_power = sum(grid.get((sx, sy), -100)
                        for sx in [x, x+1, x+2]
                        for sy in [y, y+1, y+2])
        best = max(best, (tot_power, (x, y)))

    best_x, best_y = best[1]
    answer = f'{best_x},{best_y}'

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 11)
part1(INPUT)
part2(INPUT)
