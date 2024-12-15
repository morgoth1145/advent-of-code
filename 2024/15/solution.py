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
    grid, moves = parse_input(s)
    width, height = grid.width*2, grid.height

    new_grid = {}

    start = None

    for (x, y), c in grid.items():
        if c == '#':
            new_grid[2*x,y] = '#'
            new_grid[2*x+1,y] = '#'
        if c == 'O':
            new_grid[2*x,y] = '['
            new_grid[2*x+1,y] = ']'
        if c == '.':
            new_grid[2*x,y] = '.'
            new_grid[2*x+1,y] = '.'
        if c == '@':
            new_grid[2*x,y] = '@'
            new_grid[2*x+1,y] = '.'
            start = 2*x,y

    x, y = start
    grid = new_grid

    for i, c in enumerate(moves):
        dx, dy = {'^': (0, -1),
                  'v': (0, 1),
                  '<': (-1, 0),
                  '>': (1, 0)
                  }[c]

        to_move = []
        to_check = [(x, y)]
        handled = set(to_check)
        can_move = True

        while to_check:
            srcx, srcy = to_check.pop(0)
            destx, desty = srcx+dx, srcy+dy
            c = grid[destx,desty]
            if c == '#':
                can_move = False
                break
            to_move.append((srcx, srcy, destx, desty, grid[srcx,srcy]))
            if c == '.':
                continue # Safe
            new_to_check = [(destx, desty)]
            if c == '[':
                if dx == 0:
                    new_to_check.append((destx+1, desty))
            elif c == ']':
                if dx == 0:
                    new_to_check.append((destx-1, desty))
            else:
                assert(False)

            for n in new_to_check:
                if n in handled:
                    continue
                handled.add(n)
                to_check.append(n)

        if can_move:
            while to_move:
                srcx, srcy, destx, desty, srcc = to_move.pop()
                grid[destx,desty] = srcc
                grid[srcx,srcy] = '.'

            x += dx
            y += dy

    answer = 0

    for (x, y), c in grid.items():
        if c == '[':
            answer += x + 100*y

    lib.aoc.give_answer(2024, 15, 2, answer)

INPUT = lib.aoc.get_input(2024, 15)
part1(INPUT)
part2(INPUT)
