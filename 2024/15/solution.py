import lib.aoc
import lib.grid

def parse_input(s):
    grid, moves = s.split('\n\n')

    return lib.grid.FixedGrid.parse(grid), moves.replace('\n', '')

def solve(grid, moves):
    x, y = grid.find('@')

    for c in moves:
        dx, dy = {'^': (0, -1),
                  'v': (0, 1),
                  '<': (-1, 0),
                  '>': (1, 0)}[c]

        to_move = []
        to_check = [(x, y)]
        handled = set()
        can_move = True

        while to_check:
            srcx, srcy = to_check.pop(0)
            if (srcx, srcy) in handled:
                continue
            handled.add((srcx, srcy))

            destx, desty = srcx+dx, srcy+dy

            c = grid[destx,desty]
            if c == '#':
                can_move = False
                break

            to_move.append((srcx, srcy, destx, desty))
            if c == '.':
                continue # Safe, moving into an empty tile

            to_check.append((destx, desty))
            if dx == 0:
                if c == '[':
                    to_check.append((destx+1, desty))
                elif c == ']':
                    to_check.append((destx-1, desty))

        if can_move:
            while to_move:
                srcx, srcy, destx, desty = to_move.pop()
                grid[destx,desty] = grid[srcx,srcy]
                grid[srcx,srcy] = '.'

            x, y = x+dx, y+dy

    answer = 0

    for (x, y), c in grid.items():
        if c in 'O[':
            answer += x + 100*y

    return answer

def part1(s):
    grid, moves = parse_input(s)
    answer = solve(grid, moves)

    lib.aoc.give_answer(2024, 15, 1, answer)

def widen_grid(grid):
    new_grid = {}

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

    return lib.grid.FixedGrid.from_dict(new_grid)

def part2(s):
    grid, moves = parse_input(s)
    answer = solve(widen_grid(grid), moves)

    lib.aoc.give_answer(2024, 15, 2, answer)

INPUT = lib.aoc.get_input(2024, 15)
part1(INPUT)
part2(INPUT)
