import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    answer = 0

    for y in grid.y_range:
        r = grid.row(y)
        cands = []
        for i, v in enumerate(r):
            for v2 in r[i+1:]:
                cands.append(v*10+v2)
        answer += max(cands)

    lib.aoc.give_answer(2025, 3, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 3)
part1(INPUT)
part2(INPUT)
