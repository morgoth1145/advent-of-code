import collections
import parse

import lib.aoc

def parse_lines(s):
    return parse.findall('{:d},{:d} -> {:d},{:d}', s)

def count_coord_hits(lines):
    coord_hits = collections.Counter()

    for x, y, x1, y1 in lines:
        # Any diagonals are 45 degrees so dx/dy are simple!
        dx = 1 if x1 > x else -1 if x1 < x else 0
        dy = 1 if y1 > y else -1 if y1 < y else 0

        coord_hits[x,y] += 1
        while x != x1 or y != y1:
            x += dx
            y += dy
            coord_hits[x,y] += 1

    return sum(hits > 1 for hits in coord_hits.values())

def part1(s):
    answer = count_coord_hits(filter(lambda l: l[0] == l[2] or l[1] == l[3],
                                     parse_lines(s)))
    lib.aoc.give_answer(2021, 5, 1, answer)

def part2(s):
    answer = count_coord_hits(parse_lines(s))
    lib.aoc.give_answer(2021, 5, 2, answer)

INPUT = lib.aoc.get_input(2021, 5)
part1(INPUT)
part2(INPUT)
