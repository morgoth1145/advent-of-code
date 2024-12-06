import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for pos, c in grid.items():
        if c == '^':
            start = pos
            grid[start] = '.'
            break

    x, y = start
    dx, dy = 0, -1

    seen = set()
    seen.add((x, y))

    n = x+dx, y+dy

    while n in grid:
        if grid[n] == '.':
            seen.add(n)
            x, y = n
            n = x+dx, y+dy
            continue
        assert(grid[n] == '#')
        dx, dy = -dy, dx
        n = x+dx, y+dy
        continue

    answer = len(seen)

    lib.aoc.give_answer(2024, 6, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 6)
part1(INPUT)
part2(INPUT)
