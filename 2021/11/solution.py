import lib.aoc
import lib.grid

def iterate(grid):
    flashed = set()

    for c, val in grid.items():
        grid[c] = val+1
        if val+1 > 9:
            flashed.add(c)

    to_handle = list(flashed)
    while to_handle:
        x, y = to_handle.pop(0)
        for n in grid.neighbors(x, y, diagonals=True):
            if n in flashed:
                continue
            grid[n] += 1
            if grid[n] > 9:
                flashed.add(n)
                to_handle.append(n)

    for c in flashed:
        grid[c] = 0

    return len(flashed)

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    answer = sum(iterate(grid)
                 for _ in range(100))

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    answer = 1
    while iterate(grid) != grid.area:
        answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 11)
part1(INPUT)
part2(INPUT)
