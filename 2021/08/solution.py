import collections
import itertools

import lib.aoc

def parse(s):
    for line in s.splitlines():
        inputs, outputs = line.split(' | ')
        yield inputs.split(), outputs.split()

def part1(s):
    answer = sum(len(pattern) in (2, 3, 4, 7)
                 for _, outputs in parse(s)
                 for pattern in outputs)

    print(f'The answer to part one is {answer}')

def part2(s):
    VALID_PATTERNS = {
        'abcefg':0,
        'cf':1,
        'acdeg':2,
        'acdfg':3,
        'bcdf':4,
        'abdfg':5,
        'abdefg':6,
        'acf':7,
        'abcdefg':8,
        'abcdfg':9
    }

    pattern_to_options = collections.defaultdict(set)
    mapping_options = []

    for order in itertools.permutations('abcdefg'):
        m = dict(zip('abcdefg', order))
        m_rev = dict(zip(order, 'abcdefg'))

        idx = len(mapping_options)
        mapping_options.append(m)

        for real_pattern in VALID_PATTERNS.keys():
            mangled_pattern = ''.join(sorted(m_rev[c]
                                             for c in real_pattern))
            pattern_to_options[mangled_pattern].add(idx)

    answer = 0
    for inputs, outputs in parse(s):
        candidates = set(range(len(mapping_options)))
        for pattern in inputs + outputs:
            pattern = ''.join(sorted(pattern))
            candidates &= pattern_to_options[pattern]

        assert(len(candidates) == 1)
        mapping = mapping_options[list(candidates)[0]]

        out = 0
        for n in outputs:
            new_n = ''.join(sorted(mapping[c] for c in n))
            out = out * 10 + VALID_PATTERNS[new_n]
        answer += out

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 8)
part1(INPUT)
part2(INPUT)
