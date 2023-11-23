import math

import lib.aoc

def parse_path(path):
    step = ''

    for c in path:
        if c in 'LR':
            if step != '':
                yield int(step), c
                step = ''
            else:
                yield 0, c
        else:
            step += c

    if len(step):
        yield int(step), ''

def solve(s, wrap_fn_factory):
    grid, path = s.split('\n\n')
    grid_lines = grid.splitlines()

    grid = {(x,y): val
            for y, row in enumerate(grid_lines, start=1)
            for x, val in enumerate(row, start=1)
            if val != ' '}

    width = max(map(len, grid_lines))
    height = len(grid_lines)

    wrapper = wrap_fn_factory(grid, width, height)

    x, y = s.index('.')+1, 1
    dx, dy = 1, 0

    for step, turn in parse_path(path):
        for _ in range(step):
            val = grid.get((x+dx, y+dy))
            if val == '.':
                x, y = x+dx, y+dy
                continue

            if val is None:
                # Fell off the edge, wrap around
                n, nd = wrapper(x, y, dx, dy)

                if grid[n] == '.':
                    (x, y), (dx, dy) = n, nd
                    continue

            # Hit a wall
            break

        if turn == 'R':
            dy, dx = dx, -dy
        elif turn == 'L':
            dx, dy = dy, -dx
        else:
            assert(turn == '')

    facing_val = {
        (1, 0): 0,
        (0, 1): 1,
        (-1, 0): 2,
        (0, -1): 3,
    }

    return 1000 * y + 4 * x + facing_val[dx,dy]

def simple_wrap_factory(grid, width, height):
    square_dim = math.isqrt(len(grid)//6)

    def wrap_fn(x, y, dx, dy):
        # Change nx to the opposite side of the map (plus 1 to be in bounds)
        nx, ny = x - dx * width + dx, y - dy * height + dy

        while (nx, ny) not in grid:
            nx, ny = nx + dx * square_dim, ny + dy * square_dim

        return (nx, ny), (dx, dy)

    return wrap_fn

def part1(s):
    answer = solve(s, simple_wrap_factory)

    lib.aoc.give_answer(2022, 22, 1, answer)

def cubenet_wrap_factory(grid, width, height):
    # HARDCODED FOR NOW! I literally figured this out with a cut out piece of
    # paper going through all the cases!
    def wrap_fn(x, y, dx, dy):
        if dx == 1:
            # Right
            if x == 150:
                return (100, 151-y), (-1, 0)
            if x == 100:
                if 51 <= y <= 100:
                    return (100 + (y - 50), 50), (0, -1)
                if 101 <= y <= 150:
                    return (150, 51 - (y - 100)), (-1, 0)
            if x == 50:
                return (50 + (y - 150), 150), (0, -1)
        elif dx == -1:
            # Left
            if x == 51:
                if 1 <= y <= 50:
                    return (1, 151 - y), (1, 0)
                if 51 <= y <= 100:
                    return (y - 50, 101), (0, 1)
            if x == 1:
                if 101 <= y <= 150:
                    return (51, 1 + (150 - y)), (1, 0)
                if 151 <= y <= 200:
                    return (y - 150 + 50, 1), (0, 1)
        elif dy == 1:
            # Down
            if y == 50:
                return (100, x - 50), (-1, 0)
            if y == 150:
                return (50, x + 100), (-1, 0)
            if y == 200:
                return (x + 100, 1), (0, 1)
        elif dy == -1:
            # Up
            if y == 1:
                if 51 <= x <= 100:
                    return (1, x+100), (1, 0)
                if 101 <= x <= 150:
                    return (x-100, 200), (0, -1)
            if y == 101:
                return (51, x+50), (1, 0)
        assert(False)

    return wrap_fn

def part2(s):
    answer = solve(s, cubenet_wrap_factory)

    lib.aoc.give_answer(2022, 22, 2, answer)

INPUT = lib.aoc.get_input(2022, 22)
part1(INPUT)
part2(INPUT)
