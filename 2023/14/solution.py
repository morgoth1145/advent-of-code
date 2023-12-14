import lib.aoc
import lib.grid

def ns_roll(grid, dy):
    y_range = grid.y_range[::-dy]
    for x in grid.x_range:
        dest = y_range[0]
        for y, c in zip(y_range, grid.col(x)[::-dy]):
            if c == 'O':
                if y != dest:
                    grid[x,y] = '.'
                    grid[x,dest] = 'O'
                dest -= dy
            elif c == '#':
                dest = y-dy

def ew_roll(grid, dx):
    x_range = grid.x_range[::-dx]
    for y in grid.y_range:
        dest = x_range[0]
        for x, c in zip(x_range, grid.row(y)[::-dx]):
            if c == 'O':
                if x != dest:
                    grid[x,y] = '.'
                    grid[dest,y] = 'O'
                dest -= dx
            elif c == '#':
                dest = x-dx

def calc_load(grid):
    load = 0

    for (x, y), c in grid.items():
        if c == 'O':
            load += grid.height - y

    return load

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    ns_roll(grid, -1) # North

    answer = calc_load(grid)

    lib.aoc.give_answer(2023, 14, 1, answer)

def run_cycle(grid):
    ns_roll(grid, -1) # North
    ew_roll(grid, -1) # West
    ns_roll(grid, 1) # South
    ew_roll(grid, 1) # East

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    CYCLES = 1000000000

    seen = {s:0}
    record = [s]

    cycle = 0

    while cycle < CYCLES:
        cycle += 1
        run_cycle(grid)
        key = grid.as_str('')

        if key in seen:
            last = seen[key]
            delta = cycle - last

            # Jump straight to the final answer
            cycle_off = (CYCLES - cycle) % delta
            final_state_idx = last + cycle_off

            # Reparse the final state since only the key was saved
            grid = lib.grid.FixedGrid.parse(record[final_state_idx])

            break

        seen[key] = cycle
        record.append(key)

    answer = calc_load(grid)

    lib.aoc.give_answer(2023, 14, 2, answer)

INPUT = lib.aoc.get_input(2023, 14)
part1(INPUT)
part2(INPUT)
