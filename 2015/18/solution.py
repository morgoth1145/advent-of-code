import collections

import lib.aoc
import lib.grid

def parse_grid(s):
    width = len(s.splitlines()[0])
    height = len(s.splitlines())

    on = set()

    for y, line in enumerate(s.splitlines()):
        for x, cell in enumerate(line):
            if cell == '#':
                on.add((x,y))

    return on, width, height

def step(on_cells, width, height):
    counts = collections.Counter()

    for x,y in on_cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                counts[x+dx,y+dy] += 1

    new_on = set()

    for (x,y), count in counts.items():
        if 0 <= x < width and 0 <= y < height:
            if count == 3 or (count == 2 and (x,y) in on_cells):
                new_on.add((x,y))

    return new_on

def part1(s):
    cells, width, height = parse_grid(s)

    for _ in range(100):
        cells = step(cells, width, height)

    answer = len(cells)

    print(f'The answer to part one is {answer}')

def part2(s):
    cells, width, height = parse_grid(s)

    always_on = {(0,0),
                 (0,height-1),
                 (width-1,height-1),
                 (width-1,0)}
    cells |= always_on

    for _ in range(100):
        cells = step(cells, width, height) | always_on

    answer = len(cells)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 18)
part1(INPUT)
part2(INPUT)
