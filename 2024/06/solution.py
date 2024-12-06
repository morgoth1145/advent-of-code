import lib.aoc
import lib.grid

def parse_input(s):
    grid = lib.grid.FixedGrid.parse(s)

    for pos, c in grid.items():
        if c == '^':
            grid[pos] = '.'
            return grid, pos

def part1(s):
    grid, start = parse_input(s)

    seen = set()
    seen.add(start)

    x, y = start
    dx, dy = 0, -1

    n = x+dx, y+dy

    while n in grid:
        if grid[n] == '.':
            x, y = n
            n = x+dx, y+dy
            seen.add((x, y))
            continue
        assert(grid[n] == '#')
        dx, dy = -dy, dx
        n = x+dx, y+dy
        continue

    answer = len(seen)

    lib.aoc.give_answer(2024, 6, 1, answer)

def part2(s):
    grid, start = parse_input(s)

    def steps_to_turn(x, y, dx, dy):
        steps = 0
        n = x+dx, y+dy
        while n in grid:
            if grid[n] == '#':
                return steps
            steps += 1
            x, y = n
            n = x+dx, y+dy
        return None # Sentinel to note that it leaves the board

    jumpahead = {}

    jumpahead[(start[0], start[1], 0, -1)] = steps_to_turn(*start, 0, -1)

    for (x, y), c in grid.items():
        if c == '#':
            for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                n = x-dx, y-dy # Where the guard is coming from!
                if n in grid:
                    jumpahead[n + (-dy, dx)] = steps_to_turn(*n, -dy, dx)

    def check_for_loop(cand_obstacle, x, y, dx, dy):
        obs_x, obs_y = cand_obstacle

        seen = set()

        n = x+dx, y+dy
        while n in grid:
            key = (x, y, dx, dy)
            if key in seen:
                return True
            seen.add(key)

            if key not in jumpahead:
                while n in grid and grid[n] == '.' and n != cand_obstacle:
                    x, y = n
                    n = x+dx, y+dy

                if n not in grid:
                    return False

                dx, dy = -dy, dx
                n = x+dx, y+dy
                continue

            num_steps = jumpahead[key]
            if ((dx == 0 and x == obs_x and (obs_y - y) * dy > 0) or
                (dy == 0 and y == obs_y and (obs_x - x) * dx > 0)):
                # Might hit the obstacle, check the distance
                obs_steps = max((obs_x - x) * dx, (obs_y - y) * dy) - 1

                if num_steps is None or num_steps > obs_steps:
                    # Hit the new obstacle first!
                    x += obs_steps * dx
                    y += obs_steps * dy
                    dx, dy = -dy, dx
                    n = x+dx, y+dy
                    continue

            if num_steps is None:
                return False

            x += num_steps * dx
            y += num_steps * dy
            dx, dy = -dy, dx
            n = x+dx, y+dy

    obstacle_count = 0

    seen_tiles = set()

    x, y = start
    dx, dy = 0, -1

    n = x+dx, y+dy

    # Walk the grid and check for potential obstacle locations
    while n in grid:
        seen_tiles.add((x, y))
        if grid[n] == '.':
            # If we haven't stepped on this tile yet, test it as an obstacle
            if n not in seen_tiles:
                if check_for_loop(n, x, y, dx, dy):
                    obstacle_count += 1
            x, y = n
            n = x+dx, y+dy
            continue
        assert(grid[n] == '#')
        dx, dy = -dy, dx
        n = x+dx, y+dy
        continue

    answer = obstacle_count

    lib.aoc.give_answer(2024, 6, 2, answer)

INPUT = lib.aoc.get_input(2024, 6)
part1(INPUT)
part2(INPUT)
