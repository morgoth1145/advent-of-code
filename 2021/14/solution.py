import collections

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
    pass

INPUT = lib.aoc.get_input(2021, 14)
part1(INPUT)
part2(INPUT)
