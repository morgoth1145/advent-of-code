import collections

import lib.aoc

def solve(s, iterations):
    groups = s.split('\n\n')
    s = groups[0]

    rules = {}
    for line in groups[1].split('\n'):
        left, right = line.split(' -> ')
        rules[left] = right

    counts = {pair: collections.Counter(pair)
              for pair in rules.keys()}

    for _ in range(iterations):
        new_counts = {}

        for pair, insert in rules.items():
            a, b = pair

            c = counts[a+insert] + counts[insert+b]
            c[insert] -= 1

            new_counts[pair] = c
        counts = new_counts

    c = collections.Counter()
    for i in range(len(s)-1):
        c += counts[s[i:i+2]]
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
