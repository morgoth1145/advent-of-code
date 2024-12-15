import lib.aoc
import lib.grid

def parse_input(s):
    a, b = s.split('\n\n')

    a = lib.grid.FixedGrid.parse(a)
    return a, b.replace('\n', '')

def part1(s):
    grid, moves = parse_input(s)

    x, y = grid.find('@')

    for i, c in enumerate(moves):
        dx, dy = {'^': (0, -1),
                  'v': (0, 1),
                  '<': (-1, 0),
                  '>': (1, 0)
                  }[c]

        destx, desty = x+dx, y+dy

        while grid[destx,desty] not in '.#':
            destx, desty = destx+dx, desty+dy

        if grid[destx,desty] == '#':
            # Wall, no move
            continue

        srcx, srcy = destx, desty

        while (srcx, srcy) != (x, y):
            srcx, srcy = srcx-dx, srcy-dy
            grid[destx,desty] = grid[srcx,srcy]
            destx, desty = destx-dx, desty-dy

        grid[srcx,srcy] = '.'
        x, y = x+dx, y+dy

    answer = 0

    for (x, y), c in grid.items():
        if c == 'O':
            answer += x + 100*y

    lib.aoc.give_answer(2024, 15, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 15)
part1(INPUT)
part2(INPUT)
