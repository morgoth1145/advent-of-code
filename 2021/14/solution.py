import collections
import functools

import lib.aoc

def parse(s):
    groups = s.split('\n\n')
    s = groups[0]

    rules = {}
    for line in groups[1].split('\n'):
        left, right = line.split(' -> ')
        assert(left not in rules)
        rules[left] = right

    return s, rules

def apply(s, rules):
    out = []

    last = None
    for c in s:
        if last is None:
            out.append(c)
            last = c
            continue
        pair = last + c
        insert = rules.get(pair)
        if insert is not None:
            out.append(insert)
        out.append(c)
        last = c

    return ''.join(out)

def part1(s):
    s, rules = parse(s)

    for _ in range(10):
        s = apply(s, rules)

    c = collections.Counter(s)

    most = c.most_common()[0][1]
    least = c.most_common()[-1][1]

    answer = most - least

    print(f'The answer to part one is {answer}')

def part2(s):
    s, rules = parse(s)

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
        c += figure_counts(s[i:i+2], 40)
    c -= collections.Counter(s[1:-1]) # Eliminate double-counts

    most = c.most_common()[0][1]
    least = c.most_common()[-1][1]

    answer = most - least

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 14)
part1(INPUT)
part2(INPUT)
