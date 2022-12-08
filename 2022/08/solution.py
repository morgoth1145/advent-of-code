import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    def visible(x, y):
        for dx, dy in [(-1, 0),
                       (1, 0),
                       (0, -1),
                       (0, 1)]:
            nx, ny = x+dx, y+dy
            obscured = False
            while (nx, ny) in grid:
                if grid[nx,ny] >= grid[x,y]:
                    obscured = True
                    break
                nx += dx
                ny += dy
            if not obscured:
                return True
        return False

    answer = sum(1
                 for c, _ in grid.items()
                 if visible(*c))

    lib.aoc.give_answer(2022, 8, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 8)
part1(INPUT)
part2(INPUT)
