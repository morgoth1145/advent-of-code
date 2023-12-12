import functools

import lib.aoc

@functools.cache
def count_matches(pattern, size, splits):
    if len(splits) == 0:
        if all(c in '.?' for c in pattern):
            return 1
        return 0

    a = splits[0]
    rest = splits[1:]
    after = sum(rest) + len(rest)

    count = 0

    for before in range(size-after-a+1):
        cand = '.' * before + '#' * a + '.'
        if all(c0 == c1 or c0=='?'
               for c0,c1 in zip(pattern, cand)):
            count += count_matches(pattern[len(cand):],
                                   size-a-before-1,
                                   rest)

    return count

def solve(s, copies=1):
    answer = 0

    for line in s.splitlines():
        pattern, splits = line.split()
        pattern = '?'.join((pattern,) * copies)
        splits = tuple(map(int, splits.split(','))) * copies
        answer += count_matches(pattern, len(pattern), tuple(splits))

    return answer

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2023, 12, 1, answer)

def part2(s):
    answer = solve(s, copies=5)

    lib.aoc.give_answer(2023, 12, 2, answer)

INPUT = lib.aoc.get_input(2023, 12)
part1(INPUT)
part2(INPUT)
