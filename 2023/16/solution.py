import lib.aoc
import lib.grid

import functools

def parse_contraption(s):
    grid = lib.grid.FixedGrid.parse(s)

    @functools.cache
    def shoot_to_split(x, y, dx, dy):
        traversed = []

        while True:
            traversed.append((x,y))

            c = grid[x,y]

            if c == '.':
                x, y = x+dx, y+dy
            elif c == '/':
                dx, dy = -dy, -dx
                x, y = x+dx, y+dy
            elif c == '\\':
                dx, dy = dy, dx
                x, y = x+dx, y+dy
            elif c == '|':
                if dx == 0:
                    y += dy
                else:
                    out = []
                    if y > 0:
                        out.append((x, y-1, 0, -1))
                    if y < grid.height-1:
                        out.append((x, y+1, 0, 1))
                    return traversed, out
            elif c == '-':
                if dy == 0:
                    x += dx
                else:
                    out = []
                    if x > 0:
                        out.append((x-1, y, -1, 0))
                    if x < grid.width-1:
                        out.append((x+1, y, 1, 0))
                    return traversed, out
            else:
                assert(False)

            if 0 > x or x >= grid.width or 0 > y or y >= grid.height:
                return traversed, []

    return grid.width, grid.height, shoot_to_split

def energize(shoot_to_split, x, y, dx, dy):
    good = set()
    handled = set()

    todo = [(x,y,dx,dy)]

    while todo:
        key = todo.pop()
        if key in handled:
            continue
        handled.add(key)

        traversed, out = shoot_to_split(*key)
        good.update(traversed)
        todo.extend(out)

    return len(good)

def part1(s):
    _, _, shoot_to_split = parse_contraption(s)

    answer = energize(shoot_to_split, 0, 0, 1, 0)

    lib.aoc.give_answer(2023, 16, 1, answer)

def part2(s):
    width, height, shoot_to_split = parse_contraption(s)

    options = []
    for x in range(width):
        options.append((x, 0, 0, 1))
        options.append((x, height-1, 0, -1))
    for y in range(height):
        options.append((0, y, 1, 0))
        options.append((width-1, y, -1, 0))

    answer = max(energize(shoot_to_split, *start)
                 for start in options)

    lib.aoc.give_answer(2023, 16, 2, answer)

INPUT = lib.aoc.get_input(2023, 16)
part1(INPUT)
part2(INPUT)
