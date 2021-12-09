import lib.aoc

def parse(s):
    grid = {}
    for y,row in enumerate(s.splitlines()):
        for x,val in enumerate(map(int, row)):
            grid[x,y] = val
    return grid

def neighbors(c):
    x, y = c
    yield x-1, y
    yield x+1, y
    yield x, y-1
    yield x, y+1

def part1(s):
    grid = parse(s)

    answer = 0

    for c, val in grid.items():
        if all(grid.get(n, 9) > val
               for n in neighbors(c)):
            answer += val+1

    print(f'The answer to part one is {answer}')

def count_basin_size(grid, c):
    basin = set()
    to_handle = [c]

    while to_handle:
        c = to_handle[0]
        to_handle = to_handle[1:]
        if c in basin:
            continue

        val = grid[c]
        if val == 9:
            continue

        basin.add(c)

        for n in neighbors(c):
            if grid.get(n, -5) > val:
                to_handle.append(n)

    return len(basin)

def part2(s):
    grid = parse(s)

    basin_sizes = []

    for c, val in grid.items():
        if all(grid.get(n, 9) > val
               for n in neighbors(c)):
            basin_sizes.append(count_basin_size(grid, c))

    a, b, c = sorted(basin_sizes)[-3:]
    answer = a*b*c

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 9)
part1(INPUT)
part2(INPUT)
