import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    seen = set()

    handled = set()

    todo = [(0, 0, 1, 0)]

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

    answer = len(seen)

    lib.aoc.give_answer(2023, 16, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 16)
part1(INPUT)
part2(INPUT)
