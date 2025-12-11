import functools
import math

import lib.aoc
import lib.graph

def solve(s, *valid_path_patterns):
    g = {a: b.split()
         for a, b
         in (line.split(': ')
             for line in s.splitlines())}

    lib.graph.validate_acyclic(g)

    @functools.cache
    def count_paths(pos, end):
        if pos == end:
            return 1

        return sum(count_paths(n, end)
                   for n in g.get(pos, []))

    return sum(math.prod(count_paths(a, b)
                         for a, b in zip(p, p[1:]))
               for p in valid_path_patterns)

def part1(s):
    answer = solve(s,
                   ['you', 'out'])

    lib.aoc.give_answer(2025, 11, 1, answer)

def part2(s):
    answer = solve(s,
                   ['svr', 'dac', 'fft', 'out'],
                   ['svr', 'fft', 'dac', 'out'])

    lib.aoc.give_answer(2025, 11, 2, answer)

INPUT = lib.aoc.get_input(2025, 11)
part1(INPUT)
part2(INPUT)
