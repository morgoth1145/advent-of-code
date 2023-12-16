import lib.aoc
import lib.grid

def energize(grid, x, y, dx, dy):
    good = set()
    handled = set()

    todo = [(x, y, dx, dy)]

    while todo:
        key = todo.pop()
        if key in handled:
            continue
        handled.add(key)
        x, y, dx, dy = key

        if x < 0 or x >= grid.width:
            continue
        if y < 0 or y >= grid.height:
            continue

        good.add((x,y))

        c = grid[x,y]
        if c == '.':
            todo.append((x+dx, y+dy, dx, dy))
        elif c == '/':
            todo.append((x-dy, y-dx, -dy, -dx))
        elif c == '\\':
            todo.append((x+dy, y+dx, dy, dx))
        elif c == '|':
            if dx == 0:
                todo.append((x, y+dy, 0, dy))
            else:
                todo.append((x, y-1, 0, -1))
                todo.append((x, y+1, 0, 1))
        elif c == '-':
            if dx == 0:
                todo.append((x-1, y, -1, 0))
                todo.append((x+1, y, 1, 0))
            else:
                todo.append((x+dx, y, dx, 0))
        else:
            assert(False)

    return len(good)

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = energize(grid, 0, 0, 1, 0)

    lib.aoc.give_answer(2023, 16, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    options = []
    for x in grid.x_range:
        options.append((x, 0, 0, 1))
        options.append((x, grid.height-1, 0, -1))
    for y in grid.y_range:
        options.append((0, y, 1, 0))
        options.append((grid.width-1, y, -1, 0))

    answer = max(energize(grid, *start)
                 for start in options)

    lib.aoc.give_answer(2023, 16, 2, answer)

INPUT = lib.aoc.get_input(2023, 16)
part1(INPUT)
part2(INPUT)
