import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for y in grid.y_range:
        for x in grid.x_range:
            c = grid[x,y]
            if c == 'O':
                y2 = y
                while y2 > 0:
                    if grid[x,y2-1] == '.':
                        y2 -= 1
                    else:
                        break
                grid[x,y] = '.'
                grid[x,y2] = 'O'

    answer = 0

    for (x, y), c in grid.items():
        if c == 'O':
            load = grid.height - y
            answer += load

    lib.aoc.give_answer(2023, 14, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 14)
part1(INPUT)
part2(INPUT)
