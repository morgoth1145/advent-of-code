import collections

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
        perimeter = collections.defaultdict(list)

        for x, y in sect:
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                cand = (x+dx, y+dy)
                if cand not in sect:
                    perimeter[cand].append((dx, dy))

        sides = 0

        handled = set()

        for (x, y), directs in perimeter.items():
            for dx, dy in directs:
                key = ((x, y), (dx, dy))
                if key in handled:
                    continue
                sides += 1
                for dx2, dy2 in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    if (dx2, dy2) == (dx, dy):
                        continue
                    x2, y2 = x+dx2, y+dy2
                    while (x2,y2) in perimeter:
                        if (dx, dy) not in perimeter[(x2,y2)]:
                            break
                        handled.add(((x2, y2), (dx, dy)))
                        x2 += dx2
                        y2 += dy2

        c0 = sorted(sect)[0]
        v = grid[c0]

        return sides * len(sect)

    answer = sum(map(score_section, sections))

    lib.aoc.give_answer(2024, 12, 2, answer)

INPUT = lib.aoc.get_input(2024, 12)
part1(INPUT)
part2(INPUT)
