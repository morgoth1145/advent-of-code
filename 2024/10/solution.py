import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    starts = grid.coords_by_value()[0]

    answer = 0

    def score_trailhead(coord):
        assert(grid[coord] == 0)
        seen = set()

        def impl(coord, v):
            if coord in seen:
                return
            seen.add(coord)

            if v == 9:
                yield coord
                return

            for n in grid.neighbors(*coord):
                v2 = grid[n]
                if v2 == v+1:
                    yield from impl(n, v2)

        ends = set(impl(coord, 0))
        return len(ends)

    answer = sum(map(score_trailhead, starts))

    lib.aoc.give_answer(2024, 10, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    starts = grid.coords_by_value()[0]

    answer = 0

    def score_trailhead(coord):
        assert(grid[coord] == 0)

        def impl(coord, v):
            if v == 9:
                yield coord
                return

            for n in grid.neighbors(*coord):
                v2 = grid[n]
                if v2 == v+1:
                    yield from impl(n, v2)

        ends = list(impl(coord, 0))
        return len(ends)

    answer = sum(map(score_trailhead, starts))

    lib.aoc.give_answer(2024, 10, 2, answer)

INPUT = lib.aoc.get_input(2024, 10)
part1(INPUT)
part2(INPUT)
