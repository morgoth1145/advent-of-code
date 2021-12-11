import itertools

import lib.aoc

def parse(s):
    return {(x,y): val
            for y, row in enumerate(s.splitlines())
            for x, val in enumerate(map(int, row))}

def neighbors(c):
    x, y = c
    for n in itertools.product((x-1, x, x+1),
                               (y-1, y, y+1)):
        if n != c:
            yield n

def iterate(grid):
    flashed = set()

    for c, val in grid.items():
        grid[c] = val+1
        if val+1 > 9:
            flashed.add(c)

    to_handle = list(flashed)
    while to_handle:
        c = to_handle.pop(0)
        for n in neighbors(c):
            if n not in grid or n in flashed:
                continue
            grid[n] += 1
            if grid[n] > 9:
                flashed.add(n)
                to_handle.append(n)

    for c in flashed:
        grid[c] = 0

    return len(flashed)

def part1(s):
    grid = parse(s)

    answer = sum(iterate(grid)
                 for _ in range(100))

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = parse(s)

    answer = 1
    while iterate(grid) != len(grid):
        answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 11)
part1(INPUT)
part2(INPUT)
