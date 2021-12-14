import collections
import functools

import lib.aoc

def solve(s, iterations):
    groups = s.split('\n\n')
    s = groups[0]

    rules = {}
    for line in groups[1].split('\n'):
        left, right = line.split(' -> ')
        rules[left] = right

    @functools.cache
    def figure_counts(pair, iterations):
        if iterations == 0:
            return collections.Counter(pair)

        a, b = pair
        insert = rules[pair]

        c = collections.Counter()
        c += figure_counts(a+insert, iterations-1)
        c += figure_counts(insert+b, iterations-1)
        c[insert] -= 1 # Eliminate double-counts
        return c

    c = collections.Counter()
    for i in range(len(s)-1):
        c += figure_counts(s[i:i+2], iterations)
    c -= collections.Counter(s[1:-1]) # Eliminate double-counts

    most = c.most_common()[0]
    least = c.most_common()[-1]

    return most[1] - least[1]

def part1(s):
    answer = solve(s, 10)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 40)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 14)
part1(INPUT)
part2(INPUT)
