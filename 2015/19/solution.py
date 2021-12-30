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
    rules, molecule = parse_input(s)

    steps = 0

    # Each key takes one step to add
    for key in rules.keys():
        steps += molecule.count(key)

    # Except for those in __Rn__Y__Ar, each Y gets us one for free
    steps -= molecule.count('Y')

    steps -= 1 # We start with one element

    answer = steps

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 19)
part1(INPUT)
part2(INPUT)
