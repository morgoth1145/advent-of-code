import lib.aoc
import lib.grid

def solve(s, expansion_factor):
    grid = lib.grid.FixedGrid.parse(s)

    rows_to_expand = [y
                      for y in grid.y_range
                      if set(grid.row(y)) == {'.'}]

    cols_to_expand = [x
                      for x in grid.x_range
                      if set(grid.col(x)) == {'.'}]

    def expand(x,y):
        x += sum(c < x for c in cols_to_expand) * (expansion_factor-1)
        y += sum(r < y for r in rows_to_expand) * (expansion_factor-1)
        return x,y

    galaxies = [expand(x,y)
                for (x,y), c in grid.items()
                if c == '#']

    return sum(abs(x-x2) + abs(y-y2)
               for idx, (x, y) in enumerate(galaxies)
               for x2, y2 in galaxies[idx+1:])

def part1(s):
    answer = solve(s, 2)

    lib.aoc.give_answer(2023, 11, 1, answer)

def part2(s):
    answer = solve(s, 1000000)

    lib.aoc.give_answer(2023, 11, 2, answer)

INPUT = lib.aoc.get_input(2023, 11)
part1(INPUT)
part2(INPUT)
