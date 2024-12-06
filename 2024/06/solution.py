import lib.aoc
import lib.grid

def parse_input(s):
    grid = lib.grid.FixedGrid.parse(s)

    for pos, c in grid.items():
        if c == '^':
            grid[pos] = '.'
            return grid, pos

def simulate(grid, pos, direct, previously_seen=None):
    if previously_seen is None:
        seen = set()
    else:
        seen = set(previously_seen)

    x, y = pos
    dx, dy = direct

    n = x+dx, y+dy

    while n in grid:
        key = (x, y, dx, dy)
        if key in seen:
            return 'loop', None
        seen.add(key)
        if grid[n] == '.':
            x, y = n
            n = x+dx, y+dy
            continue
        assert(grid[n] == '#')
        dx, dy = -dy, dx
        n = x+dx, y+dy
        continue

    # Ensure that the final tile is counted!
    key = (x, y, dx, dy)
    seen.add(key)

    return 'exit', len(set((x,y) for x,y,dx,dy in seen))

def part1(s):
    grid, start = parse_input(s)

    res, walked_tiles = simulate(grid, start, (0, -1))
    assert(res == 'exit')

    answer = walked_tiles

    lib.aoc.give_answer(2024, 6, 1, answer)

def part2(s):
    grid, start = parse_input(s)

    good_obstacles = set()

    seen_states = set()
    seen_tiles = set()

    x, y = start
    dx, dy = 0, -1

    n = x+dx, y+dy

    while n in grid:
        seen_tiles.add((x, y))
        key = (x, y, dx, dy)
        if grid[n] == '.':
            # Test the obstacle location (if it's not one we've stepped on,
            # can't block part of the historical path!)
            if n not in seen_tiles:
                grid[n] = '#'
                if simulate(grid, (x, y), (dx, dy), seen_states)[0] == 'loop':
                    good_obstacles.add(n)
                grid[n] = '.'
            seen_states.add(key)
            x, y = n
            n = x+dx, y+dy
            continue
        seen_states.add(key)
        assert(grid[n] == '#')
        dx, dy = -dy, dx
        n = x+dx, y+dy
        continue

    answer = len(good_obstacles)

    lib.aoc.give_answer(2024, 6, 2, answer)

INPUT = lib.aoc.get_input(2024, 6)
part1(INPUT)
part2(INPUT)
