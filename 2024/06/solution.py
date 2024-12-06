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
    grid = lib.grid.FixedGrid.parse(s)

    for pos, c in grid.items():
        if c == '^':
            start = pos
            grid[start] = '.'
            break

    good_obstacles = set()

    def check_if_loops():
        x, y = start
        dx, dy = 0, -1

        seen = set()

        n = x+dx, y+dy

        while n in grid:
            key = (x, y, dx, dy)
            if key in seen:
                return True
            seen.add(key)
            if grid[n] == '.':
                x, y = n
                n = x+dx, y+dy
                continue
            assert(grid[n] == '#')
            dx, dy = -dy, dx
            n = x+dx, y+dy
            continue

        return False

    for i, (cand_obstacle, old_c) in enumerate(grid.items()):
        if i % 100 == 0:
            print(i, grid.width*grid.height)
        if old_c == '#':
            continue
        grid[cand_obstacle] = '#'
        if check_if_loops():
            good_obstacles.add(cand_obstacle)
        grid[cand_obstacle] = old_c

    answer = len(good_obstacles)

    lib.aoc.give_answer(2024, 6, 2, answer)

INPUT = lib.aoc.get_input(2024, 6)
part1(INPUT)
part2(INPUT)
