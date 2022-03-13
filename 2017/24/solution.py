import collections
import functools

import lib.aoc

def solve(s, maximize_length):
    parts = []
    connections = collections.defaultdict(set)

    for idx, line in enumerate(s.splitlines()):
        a, b = line.split('/')
        a, b = int(a), int(b)
        connections[a].add(idx)
        connections[b].add(idx)
        parts.append((a, b))

    @functools.cache
    def strongest(port, used):
        candidates = connections[port] - set(used)

        if maximize_length:
            best = (0, 0)
        else:
            best = 0

        for idx in candidates:
            a, b = parts[idx]
            if a == port:
                other = b
            else:
                other = a
                assert(b == port)

            strength = strongest(other, tuple(sorted(used + (idx,))))

            if maximize_length:
                length, strength = strength
                best = max(best, (length+1, a + b + strength))
            else:
                best = max(best, a + b + strength)

        return best

    best = strongest(0, tuple())
    if maximize_length:
        best = best[1]

    return best

def part1(s):
    answer = solve(s, maximize_length=False)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, maximize_length=True)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 24)
part1(INPUT)
part2(INPUT)
