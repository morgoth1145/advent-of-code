import lib.aoc
import lib.grid

def step(grid):
    new_state = {}

    for (x, y), val in grid.items():
        count = 0
        for n in grid.neighbors(x, y, diagonals=True):
            if grid[n] == '#':
                count += 1
        if val == '#' and count in (2, 3):
            new_state[x,y] = '#'
        elif val == '.' and count == 3:
            new_state[x,y] = '#'
        else:
            new_state[x,y] = '.'

    return lib.grid.FixedGrid.from_dict(new_state)

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for _ in range(100):
        grid = step(grid)

    answer = sum(1
                 for _, val in grid.items()
                 if val == '#')

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 18)
part1(INPUT)
part2(INPUT)
