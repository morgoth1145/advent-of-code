import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = 0

    for (x, y), c in grid.items():
        if c != 'X':
            continue
        for dx, dy in [(1, 0), (0, 1), (1, 1),
                       (-1, 0), (0, -1), (-1, -1),
                       (1, -1), (-1, 1)]:
            x1 = x+dx
            y1 = y+dy
            x2 = x1+dx
            y2 = y1+dy
            x3 = x2+dx
            y3 = y2+dy
            if not (x3, y3) in grid:
                continue
            if grid[x1,y1] == 'M' and grid[x2,y2] == 'A' and grid[x3,y3] == 'S':
                answer += 1

    lib.aoc.give_answer(2024, 4, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 4)
part1(INPUT)
part2(INPUT)
