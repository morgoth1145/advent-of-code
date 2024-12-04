import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = 0

    for (x, y), c in grid.items():
        if c != 'X':
            continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 == dy:
                    continue
                if (x+3*dx, y+3*dy) not in grid:
                    continue
                if all(grid[x+i*dx, y+i*dy] == c2
                       for i, c2 in enumerate('MAS', start=1)):
                    answer += 1

    lib.aoc.give_answer(2024, 4, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = 0

    for (x, y), c in grid.items():
        if c != 'A':
            continue
        is_xmas = True
        for dx, dy in [(1, 1), (1, -1)]:
            n1 = x+dx, y+dy
            n2 = x-dx, y-dy
            if n1 not in grid or n2 not in grid:
                is_xmas = False
                break
            # Check if the diagonal makes "MAS"
            if set(grid[n1] + grid[n2]) != set('MS'):
                is_xmas = False
                break
        if is_xmas:
            answer += 1

    lib.aoc.give_answer(2024, 4, 2, answer)

INPUT = lib.aoc.get_input(2024, 4)
part1(INPUT)
part2(INPUT)
