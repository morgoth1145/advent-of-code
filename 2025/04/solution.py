import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = 0

    for pos, c in grid.items():
        if c != '@':
            continue
        adj = 0
        for n in grid.neighbors(*pos, diagonals=True):
            if grid[n] == '@':
                adj += 1

        if adj < 4:
            answer += 1

    lib.aoc.give_answer(2025, 4, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 4)
part1(INPUT)
part2(INPUT)
