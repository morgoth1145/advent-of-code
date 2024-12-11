import collections

import lib.aoc

def solve(s, num_cycles):
    counts = collections.Counter(map(int, s.split()))

    for _ in range(num_cycles):
        new_counts = collections.Counter()

        for v, c in counts.items():
            if v == 0:
                new_counts[1] += c
                continue
            s = str(v)
            if len(s) % 2 == 0:
                left = int(s[:len(s)//2])
                right = int(s[len(s)//2:])
                new_counts[left] += c
                new_counts[right] += c
            else:
                new_counts[v*2024] += c

        counts = new_counts

    return sum(counts.values())

def part1(s):
    answer = solve(s, 25)

    lib.aoc.give_answer(2024, 11, 1, answer)

def part2(s):
    answer = solve(s, 75)

    lib.aoc.give_answer(2024, 11, 2, answer)

INPUT = lib.aoc.get_input(2024, 11)
part1(INPUT)
part2(INPUT)
