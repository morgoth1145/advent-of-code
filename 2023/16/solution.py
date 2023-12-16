import lib.aoc
import lib.grid

def energize(grid, x, y, dx, dy):
    seen = set()

    handled = set()

    todo = [(x, y, dx, dy)]

    def visit(x, y, dx, dy):
        key = (x, y, dx, dy)
        todo.append(key)

    while todo:
        key = todo.pop(-1)
        if key in handled:
            continue
        handled.add(key)
        x, y, dx, dy = key

        if x < 0 or x >= grid.width:
            continue
        if y < 0 or y >= grid.height:
            continue
        seen.add((x,y))

        c = grid[x,y]
        if c == '.':
            visit(x+dx, y+dy, dx, dy)
            continue
        elif c in '/\\':
            # Mirror
            if c == '/':
                if dx != 0:
                    # Left turn
                    dx, dy = 0, -dx
                else:
                    # Right turn
                    dx, dy = -dy, 0
            elif c == '\\':
                if dy != 0:
                    # Left turn
                    dx, dy = dy, 0
                else:
                    # Right turn
                    dx, dy = 0, dx
            visit(x+dx, y+dy, dx, dy)
            continue
        elif c in '|-':
            # Splitter
            if c == '|':
                if dy != 0:
                    visit(x+dx, y+dy, dx, dy)
                    continue
                else:
                    visit(x, y-1, 0, -1)
                    visit(x, y+1, 0, 1)
                    continue
            elif c == '-':
                if dx != 0:
                    visit(x+dx, y+dy, dx, dy)
                    continue
                else:
                    visit(x-1, y, -1, 0)
                    visit(x+1, y, 1, 0)
                    continue
            else:
                assert(False)
            pass
        else:
            assert(False)

    return len(seen)

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
