import collections

import lib.aoc
import lib.grid

def step(grid):
    has_bug = set(coord
                  for coord, c in grid.items()
                  if c == '#')

    for (x, y), c in grid.items():
        neighbor_bugs = sum(1 for n in grid.neighbors(x, y)
                            if n in has_bug)
        if c == '#' and neighbor_bugs != 1:
            # Bug died
            grid[x,y] = '.'
        elif c == '.' and neighbor_bugs in (1, 2):
            # Infested
            grid[x,y] = '#'

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    seen = set()
    seen.add(grid.as_str())

    while True:
        step(grid)

        key = grid.as_str()
        if key in seen:
            break

        seen.add(key)

    answer = 0

    for (x, y), c in grid.items():
        if c == '#':
            biodiversity = 2 ** (x + y * grid.width)
            answer += biodiversity

    lib.aoc.give_answer(2019, 24, 1, answer)

def recursive_step(bugs):
    neighbor_counts = collections.Counter()

    for x, y, level in bugs:
        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if (nx, ny) == (2, 2):
                # Recurses down to level-1
                if x == 1:
                    # Coming from the left
                    for ny in range(5):
                        neighbor_counts[0,ny,level-1] += 1
                    continue

                if x == 3:
                    # Coming from the right
                    for ny in range(5):
                        neighbor_counts[4,ny,level-1] += 1
                    continue

                if y == 1:
                    # Coming from the top
                    for nx in range(5):
                        neighbor_counts[nx,0,level-1] += 1
                    continue

                if y == 3:
                    # Coming from the bottom
                    for nx in range(5):
                        neighbor_counts[nx,4,level-1] += 1
                    continue

                # This shouldn't be possible
                assert(False)

            if nx == -1:
                # Recurses up to level+1
                neighbor_counts[1,2,level+1] += 1
                continue

            if nx == 5:
                # Recurses up to level+1
                neighbor_counts[3,2,level+1] += 1
                continue

            if ny == -1:
                # Recurses up to level+1
                neighbor_counts[2,1,level+1] += 1
                continue

            if ny == 5:
                # Recurses up to level+1
                neighbor_counts[2,3,level+1] += 1
                continue

            assert(nx >= 0 and nx < 5 and ny >= 0 and ny < 5)

            # Just a normal neighbor. Yay!
            neighbor_counts[nx,ny,level] += 1
            continue

    return set(coord
               for coord, count in neighbor_counts.items()
               if count == 1 or (count == 2 and coord not in bugs))

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    bugs = set((x, y, 0)
               for (x, y), c in grid.items()
               if c == '#' and (x, y) != (2, 2))

    for _ in range(200):
        bugs = recursive_step(bugs)

    answer = len(bugs)

    lib.aoc.give_answer(2019, 24, 2, answer)

INPUT = lib.aoc.get_input(2019, 24)
part1(INPUT)
part2(INPUT)
