import functools

import lib.aoc

@functools.cache
def count_matches(pattern, splits):
    a = splits[0]
    rest = splits[1:]
    after = sum(rest) + len(rest)

    count = 0

    for before in range(len(pattern)-after-a+1):
        if all(c in '#?' for c in pattern[before:before+a]):
            if len(rest) == 0:
                if all(c in '.?' for c in pattern[before+a:]):
                    count += 1
            elif pattern[before+a] in '.?':
                count += count_matches(pattern[before+a+1:], rest)

        if pattern[before] not in '.?':
            break

    return count

def solve(s, copies=1):
    answer = 0

    for line in s.splitlines():
        pattern, splits = line.split()
        pattern = '?'.join((pattern,) * copies)
        splits = tuple(map(int, splits.split(','))) * copies
        answer += count_matches(pattern, tuple(splits))

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
