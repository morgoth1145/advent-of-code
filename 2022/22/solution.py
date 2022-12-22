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
    pass

INPUT = lib.aoc.get_input(2022, 22)
part1(INPUT)
part2(INPUT)
