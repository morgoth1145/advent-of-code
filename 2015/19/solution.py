import collections

import lib.aoc

def parse_input(s):
    g0, molecule = s.split('\n\n')

    rules = collections.defaultdict(list)
    for line in g0.splitlines():
        left, right = line.split(' => ')
        assert(len(left) <= len(right))
        rules[left].append(right)

    return rules, molecule

def part1(s):
    rules, molecule = parse_input(s)

    possibilities = set()

    for base, replacements in rules.items():
        last_idx = 0
        while True:
            idx = molecule.find(base, last_idx)
            if idx == -1:
                break
            for repl in replacements:
                new = molecule[:idx] + repl + molecule[idx+len(base):]
                possibilities.add(new)
            last_idx = idx + len(base)

    answer = len(possibilities)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 19)
part1(INPUT)
part2(INPUT)
