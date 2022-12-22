import lib.aoc

def parse_input(s):
    groups = s.split('\n\n')

    start = None

    grid = {}
    for y, row in enumerate(groups[0].splitlines(), start=1):
        for x, val in enumerate(row, start=1):
            if val in '.#':
                if start is None:
                    start = (x, y)
                grid[x,y] = val

    path = []
    last = ''
    for c in groups[1]:
        if c in 'LR':
            if last != '':
                path.append(int(last))
                last = ''
            path.append(c)
        else:
            last += c
    if last != '':
        path.append(int(last))

    return grid, path, start

# dx, dy
facing_val = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}

def part1(s):
    grid, path, (x, y) = parse_input(s)

    dx = 1
    dy = 0

    for step in path:
        if isinstance(step, int):
            for _ in range(step):
                nx, ny = x+dx, y+dy
                cell = grid.get((nx, ny))
                if cell is None:
                    # WRAP
                    nnx, nny = x, y
                    while (nnx, nny) in grid:
                        nx, ny = nnx, nny
                        nnx -= dx
                        nny -= dy
                    cell = grid[nx,ny]
                if cell == '#':
                    break # Hit a wall!
                x, y = nx, ny
        elif step == 'R':
            dy, dx = dx, -dy
        elif step == 'L':
            dx, dy = dy, -dx
        else:
            assert(False)

    answer = 1000 * y + 4 * x + facing_val[dx,dy]

    lib.aoc.give_answer(2022, 22, 1, answer)

def part2(s):
    grid, path, (x, y) = parse_input(s)

    # HARDCODED FOR NOW! I literally figured this out with a cut out piece of
    # paper going through all the cases!
    def wrap(x, y, dx, dy):
        if dx == 1:
            # Right
            if x == 150:
                return 100, 151-y, -1, 0
            if x == 100:
                if 51 <= y <= 100:
                    return 100 + (y - 50), 50, 0, -1
                if 101 <= y <= 150:
                    return 150, 51 - (y - 100), -1, 0
            if x == 50:
                return 50 + (y - 150), 150, 0, -1
        elif dx == -1:
            # Left
            if x == 51:
                if 1 <= y <= 50:
                    return 1, 151 - y, 1, 0
                if 51 <= y <= 100:
                    return y - 50, 101, 0, 1
            if x == 1:
                if 101 <= y <= 150:
                    return 51, 1 + (150 - y), 1, 0
                if 151 <= y <= 200:
                    return y - 150 + 50, 1, 0, 1
        elif dy == 1:
            # Down
            if y == 50:
                return 100, x - 50, -1, 0
            if y == 150:
                return 50, x + 100, -1, 0
            if y == 200:
                return x + 100, 1, 0, 1
        elif dy == -1:
            # Up
            if y == 1:
                if 51 <= x <= 100:
                    return 1, x+100, 1, 0
                if 101 <= x <= 150:
                    return x-100, 200, 0, -1
            if y == 101:
                return 51, x+50, 1, 0
        assert(False)

    dx = 1
    dy = 0

    for step in path:
        if isinstance(step, int):
            for _ in range(step):
                nx, ny = x+dx, y+dy
                cell = grid.get((nx, ny))
                if cell is None:
                    # WRAP
                    nx, ny, ndx, ndy = wrap(x, y, dx, dy)

                    # Debugging!
                    if (nx, ny) not in grid:
                        print(x, y, dx, dy)
                        print(nx, ny)

                    # Got the wrong answer initially meaning I had some wrapping
                    # wrong. Thankfully checking the inverse of the wrap (it
                    # should be invertible) found the error!
                    try:
                        revx, revy, revdx, revdy = wrap(nx, ny, -ndx, -ndy)
                        if (revx, revy, -revdx, -revdy) != (x, y, dx, dy):
                            print(x, y, dx, dy)
                            print(nx, ny, -ndx, -ndy)
                            print(revx, revy, -revdx, -revdy)
                            assert(False)
                    except:
                        assert(False)

                    cell = grid[nx,ny]
                    if cell == '#':
                        break # Hit a wall, don't mess with direction
                    x, y = nx, ny
                    dx, dy = ndx, ndy
                elif cell == '#':
                    break # Hit a wall!
                x, y = nx, ny
        elif step == 'R':
            dy, dx = dx, -dy
        elif step == 'L':
            dx, dy = dy, -dx
        else:
            assert(False)

    answer = 1000 * y + 4 * x + facing_val[dx,dy]

    lib.aoc.give_answer(2022, 22, 2, answer)

INPUT = lib.aoc.get_input(2022, 22)
part1(INPUT)
part2(INPUT)
