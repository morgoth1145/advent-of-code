import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    seen = set()

    sections = []

    def fill_section(coord):
        v = grid[coord]
        sect = set()

        to_handle = [coord]

        while to_handle:
            p = to_handle.pop()
            sect.add(p)
            for n in grid.neighbors(*p):
                if n in seen:
                    continue
                nv = grid[n]
                if nv == v:
                    seen.add(n)
                    to_handle.append(n)

        seen.update(sect)
        sections.append(sect)

    for coord, c in grid.items():
        if coord in seen:
            continue
        fill_section(coord)

    answer = 0

    def score_section(sect):
        perimeter = 0

        for x, y in sect:
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                cand = (x+dx, y+dy)
                if cand not in sect:
                    perimeter += 1

        v = grid[sorted(sect)[0]]

        return perimeter * len(sect)

    answer = sum(map(score_section, sections))

    lib.aoc.give_answer(2024, 12, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 12)
part1(INPUT)
part2(INPUT)
