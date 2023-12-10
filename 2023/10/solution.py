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
    pass

INPUT = lib.aoc.get_input(2023, 10)
part1(INPUT)
part2(INPUT)
