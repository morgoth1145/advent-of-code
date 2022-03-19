import lib.aoc
import lib.grid

def step(grid):
    start_state = grid.to_dict()

    for (x, y), val in grid.items():
        ground = 0
        trees = 0
        lumber = 0
        for n in grid.neighbors(x, y, diagonals=True):
            nval = start_state[n]
            if nval == '.':
                ground += 1
            elif nval == '|':
                trees += 1
            elif nval == '#':
                lumber += 1
            else:
                assert(False)
        if val == '.':
            if trees >= 3:
                grid[x,y] = '|'
        elif val == '|':
            if lumber >= 3:
                grid[x,y] = '#'
        elif val == '#':
            if lumber < 1 or trees < 1:
                grid[x,y] = '.'
        else:
            assert(False)

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for _ in range(10):
        step(grid)

    wooded = sum(1 for c, val in grid.items()
                 if val == '|')
    lumber = sum(1 for c, val in grid.items()
                 if val == '#')

    answer = wooded * lumber

    print(f'The answer to part one is {answer}')

def part2(s):
    TARGET = 1000000000

    grid = lib.grid.FixedGrid.parse(s)

    seen = {
        grid.as_str(''): 0
    }
    order = [grid.as_str('')]

    step_num = 0
    while step_num < TARGET:
        step_num += 1
        step(grid)
        key = grid.as_str('')
        if key in seen:
            last_step = seen[key]
            jump_by = step_num - last_step
            remaining = TARGET - step_num
            final_idx = last_step + (remaining % jump_by)
            final_key = order[final_idx]
            break

        seen[key] = step_num
        order.append(key)

    wooded = final_key.count('|')
    lumber = final_key.count('#')

    answer = wooded * lumber

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 18)
part1(INPUT)
part2(INPUT)
