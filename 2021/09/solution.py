import lib.aoc

def parse(s):
    grid = []
    for line in s.splitlines():
        grid.append(list(map(int, line)))
    return grid

def part1(s):
    grid = parse(s)

    answer = 0

    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if x > 0:
                if grid[x-1][y] <= val:
                    continue
            if x < len(grid)-1:
                if grid[x+1][y] <= val:
                    continue
            if y > 0:
                if row[y-1] <= val:
                    continue
            if y < len(row)-1:
                if row[y+1] <= val:
                    continue
            answer += val+1

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = parse(s)

    handled = set()
    for x,row in enumerate(grid):
        for y,val in enumerate(row):
            if val == 9:
                handled.add((x,y))

    remaining = {(x,y)
                 for x,row in enumerate(grid)
                 for y in range(len(row))} - handled

    basin_sizes = []

    while len(remaining):
        basin = set()
        c = list(remaining)[0]
        to_handle = [c]
        while to_handle:
            c = to_handle[0]
            to_handle = to_handle[1:]

            if c in handled or c in basin:
                continue

            basin.add(c)
            x,y = c

            if x > 0:
                to_handle.append((x-1,y))
            if x < len(grid)-1:
                to_handle.append((x+1,y))
            if y > 0:
                to_handle.append((x,y-1))
            if y < len(grid[x])-1:
                to_handle.append((x,y+1))

        basin_sizes.append(len(basin))
        handled |= basin
        remaining -= basin

    a, b, c = sorted(basin_sizes)[-3:]
    answer = a*b*c

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 9)
part1(INPUT)
part2(INPUT)
