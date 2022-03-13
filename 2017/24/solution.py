import collections
import functools

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split('/')
        yield int(a), int(b)

def part1(s):
    parts = list(parse_input(s))

    port_to_indices = collections.defaultdict(set)
    for idx, (a, b) in enumerate(parts):
        port_to_indices[a].add(idx)
        port_to_indices[b].add(idx)

    @functools.cache
    def strongest(port, used):
        candidates = port_to_indices[port] - set(used)

        best = 0

        for idx in candidates:
            a, b = parts[idx]
            if a == port:
                other = b
            else:
                other = a
                assert(b == port)

            strength = a+b + strongest(other, tuple(sorted(used + (idx,))))
            best = max(best, strength)

        return best

    answer = strongest(0, tuple())

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 24)
part1(INPUT)
part2(INPUT)
