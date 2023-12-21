import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    positions = [start]

    for i in range(64):
        next_positions = set()

        for p in positions:
            next_positions.update(grid.neighbors(*p))

        positions = [p for p in next_positions
                     if grid[p] != '#']

    answer = len(positions)

    lib.aoc.give_answer(2023, 21, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 21)
part1(INPUT)
part2(INPUT)
