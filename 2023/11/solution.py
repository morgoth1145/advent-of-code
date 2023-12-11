import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    rows_without_galaxies = []
    for y in range(grid.height):
        if all(grid[x,y] == '.' for x in range(grid.width)):
            rows_without_galaxies.append(y)

    cols_without_galaxies = []
    for x in range(grid.width):
        if all(grid[x,y] == '.' for y in range(grid.height)):
            cols_without_galaxies.append(x)

    def adjust(x,y):
        x += sum(c < x
                 for c in cols_without_galaxies)
        y += sum(r < y
                 for r in rows_without_galaxies)
        return x,y

    galaxies = [adjust(x,y)
                for (x,y), c in grid.items()
                if c == '#']

    answer = 0

    for idx, (x, y) in enumerate(galaxies):
        for x2, y2 in galaxies[idx+1:]:
            answer += abs(x-x2) + abs(y-y2)

    lib.aoc.give_answer(2023, 11, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 11)
part1(INPUT)
part2(INPUT)
