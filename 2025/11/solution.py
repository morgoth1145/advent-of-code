import functools

import lib.aoc

def parse_input(s):
    g = {}

    for line in s.splitlines():
        a, b = line.split(': ')
        g[a] = set(b.split())

    return g

def part1(s):
    g = parse_input(s)

    @functools.cache
    def count_paths(pos, seen):
        if pos == 'out':
            return 1

        seen = set(seen)

        total = 0
        for n in g[pos]:
            if n in seen:
                continue
            seen.add(n)
            total += count_paths(n, tuple(sorted(seen)))
            seen.remove(n)

        return total

    answer = count_paths('you', tuple())

    lib.aoc.give_answer(2025, 11, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 11)
part1(INPUT)
part2(INPUT)
