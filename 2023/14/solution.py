import lib.aoc
import lib.grid

def calc_load(grid):
    load = 0

    for (x, y), c in grid.items():
        if c == 'O':
            load += grid.height - y

    return load

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for y in grid.y_range:
        for x in grid.x_range:
            c = grid[x,y]
            if c == 'O':
                y2 = y
                while y2 > 0:
                    if grid[x,y2-1] == '.':
                        y2 -= 1
                    else:
                        break
                grid[x,y] = '.'
                grid[x,y2] = 'O'

    answer = calc_load(grid)

    lib.aoc.give_answer(2023, 14, 1, answer)

def run_cycle(grid):
    # North
    for y in grid.y_range:
        for x in grid.x_range:
            c = grid[x,y]
            if c == 'O':
                y2 = y
                while y2 > 0:
                    if grid[x,y2-1] == '.':
                        y2 -= 1
                    else:
                        break
                grid[x,y] = '.'
                grid[x,y2] = 'O'

    # West
    for y in grid.y_range:
        for x in grid.x_range:
            c = grid[x,y]
            if c == 'O':
                x2 = x
                while x2 > 0:
                    if grid[x2-1,y] == '.':
                        x2 -= 1
                    else:
                        break
                grid[x,y] = '.'
                grid[x2,y] = 'O'

    # South
    for y in grid.y_range[::-1]:
        for x in grid.x_range:
            c = grid[x,y]
            if c == 'O':
                y2 = y
                while y2 < grid.height-1:
                    if grid[x,y2+1] == '.':
                        y2 += 1
                    else:
                        break
                grid[x,y] = '.'
                grid[x,y2] = 'O'

    # East
    for y in grid.y_range:
        for x in grid.x_range[::-1]:
            c = grid[x,y]
            if c == 'O':
                x2 = x
                while x2 < grid.width-1:
                    if grid[x2+1,y] == '.':
                        x2 += 1
                    else:
                        break
                grid[x,y] = '.'
                grid[x2,y] = 'O'

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    CYCLES = 1000000000

    seen = {grid.as_str(''):0}

    cycle = 0

    while cycle < CYCLES:
        cycle += 1
        run_cycle(grid)
        key = grid.as_str('')

        if key in seen:
            delta = cycle - seen[key]
            rem = CYCLES - cycle
            time_skip = (rem // delta) * delta
            cycle += time_skip
            break

        seen[key] = cycle

    while cycle < CYCLES:
        cycle += 1
        run_cycle(grid)

    answer = calc_load(grid)

    lib.aoc.give_answer(2023, 14, 2, answer)

INPUT = lib.aoc.get_input(2023, 14)
part1(INPUT)
part2(INPUT)
