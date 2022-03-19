import lib.aoc
import lib.grid

def step(grid):
    start_state = grid.to_dict()

    for (x, y), val in grid.items():
        ground = 0
        trees = 0
        lumber = 0
        for n in grid.neighbors(x, y, diagonals=True):
            nval = start_state[n]
            if nval == '.':
                ground += 1
            elif nval == '|':
                trees += 1
            elif nval == '#':
                lumber += 1
            else:
                assert(False)
        if val == '.':
            if trees >= 3:
                grid[x,y] = '|'
        elif val == '|':
            if lumber >= 3:
                grid[x,y] = '#'
        elif val == '#':
            if lumber < 1 or trees < 1:
                grid[x,y] = '.'
        else:
            assert(False)

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for _ in range(10):
        step(grid)

    wooded = sum(1 for c, val in grid.items()
                 if val == '|')
    lumber = sum(1 for c, val in grid.items()
                 if val == '#')

    answer = wooded * lumber

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 18)
part1(INPUT)
part2(INPUT)
