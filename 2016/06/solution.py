import collections

import lib.aoc

def part1(s):
    columns = collections.defaultdict(collections.Counter)

    for line in s.splitlines():
        for idx, c in enumerate(line):
            columns[idx][c] += 1

    answer = ''

    for idx, c in sorted(columns.items()):
        answer += c.most_common(1)[0][0]

    print(f'The answer to part one is {answer}')

def part2(s):
    columns = collections.defaultdict(collections.Counter)

    for line in s.splitlines():
        for idx, c in enumerate(line):
            columns[idx][c] += 1

    answer = ''

    for idx, c in sorted(columns.items()):
        answer += c.most_common()[-1][0]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 6)
part1(INPUT)
part2(INPUT)
