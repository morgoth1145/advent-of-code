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

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 24)
part1(INPUT)
part2(INPUT)
