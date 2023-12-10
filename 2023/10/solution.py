import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = [coord
             for coord, c in grid.items()
             if c == 'S'][0]

    positions = [start]
    seen = set()

    answer = 0

    def get_connections(x,y):
        c = grid[x,y]
        if c == '|':
            return [(x,y-1),
                     (x,y+1)]
        elif c == '-':
            return [(x-1,y),
                     (x+1,y)]
        elif c == 'L':
            return [(x,y-1),
                     (x+1,y)]
        elif c == 'J':
            return [(x,y-1),
                     (x-1,y)]
        elif c == '7':
            return [(x-1,y),
                     (x,y+1)]
        elif c == 'F':
            return [(x+1,y),
                     (x,y+1)]
        else:
            assert(False)

    while positions:
        seen.update(positions)
        next_positions = set()

        for x,y in positions:
            c = grid[x,y]
            cands = []
            if c == 'S':
                for n in [(x-1,y),
                         (x+1,y),
                         (x,y-1),
                         (x,y+1)]:
                    if n not in grid:
                        continue
                    if grid[n] == '.':
                        continue
                    if (x,y) in get_connections(*n):
                        cands.append(n)
            else:
                cands = get_connections(x,y)

            for n in cands:
                if n not in grid:
                    continue
                if n in seen:
                    continue
                assert(grid[n] != '.')
                next_positions.add(n)

        positions = list(next_positions)
        if len(positions) > 0:
            answer += 1

    lib.aoc.give_answer(2023, 10, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = [coord
             for coord, c in grid.items()
             if c == 'S'][0]

    positions = [start]
    seen = set()
    edges = []

    def get_connections(x,y):
        c = grid[x,y]
        if c == '|':
            return [(x,y-1),
                     (x,y+1)]
        elif c == '-':
            return [(x-1,y),
                     (x+1,y)]
        elif c == 'L':
            return [(x,y-1),
                     (x+1,y)]
        elif c == 'J':
            return [(x,y-1),
                     (x-1,y)]
        elif c == '7':
            return [(x-1,y),
                     (x,y+1)]
        elif c == 'F':
            return [(x+1,y),
                     (x,y+1)]
        else:
            assert(False)

    while positions:
        seen.update(positions)
        next_positions = set()

        for x,y in positions:
            c = grid[x,y]
            cands = []
            if c == 'S':
                for n in [(x-1,y),
                         (x+1,y),
                         (x,y-1),
                         (x,y+1)]:
                    if n not in grid:
                        continue
                    if grid[n] == '.':
                        continue
                    if (x,y) in get_connections(*n):
                        cands.append(n)
            else:
                cands = get_connections(x,y)

            for n in cands:
                if n not in grid:
                    continue
                if n in seen:
                    continue
                assert(grid[n] != '.')
                next_positions.add(n)
                edges.append(((x,y),n))

        positions = list(next_positions)

    loop = set()
    for (x, y), (x2, y2) in edges:
        loop.add((2*x,2*y))
        loop.add((2*x2,2*y2))
        loop.add((x+x2,y+y2))

    handled = set(loop)

    contained = set()

    for (x,y), c in grid.items():
        x *= 2
        y *= 2
        if (x,y) in handled:
            continue

        coord = x,y

        expanded = {(x,y)}
        to_handle = [(x,y)]
        escaped = False

        while to_handle:
            x,y = to_handle.pop(-1)

            for nx,ny in [(x-1,y),
                      (x+1,y),
                      (x,y+1),
                      (x,y-1)]:
                n = nx,ny
                if nx < 0 or nx > (grid.width * 2) - 2:
                    escaped = True
                    continue
                if ny < 0 or ny > (grid.height * 2) - 2:
                    escaped = True
                    continue
                if n in handled:
                    continue
                if n in expanded:
                    continue
                to_handle.append(n)
                expanded.add(n)

        handled.update(expanded)

        if coord == (6,6):
            print(escaped)

        if not escaped:
            contained.update(expanded)

    real_contained = [(x//2,y//2)
                      for x,y in contained
                      if x % 2 == 0 and y % 2 == 0]

    answer = len(real_contained)

    lib.aoc.give_answer(2023, 10, 2, answer)

INPUT = lib.aoc.get_input(2023, 10)
part1(INPUT)
part2(INPUT)
