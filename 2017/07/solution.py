import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        bits = line.split(' -> ')
        a, b = bits[0].split()
        assert(b[0] == '(' and b[-1] == ')')
        b = int(b[1:-1])
        if len(bits) == 2:
            rest = bits[1].split(', ')
        else:
            rest = []
        yield a, b, rest

def part1(s):
    seen = set()
    referenced = set()

    for name, weight, held in parse_input(s):
        seen.add(name)
        referenced.update(held)

    base = list(seen - referenced)
    assert(len(base) == 1)

    answer = base[0]

    print(f'The answer to part one is {answer}')

def part2(s):
    seen = set()
    referenced = set()

    tree = {}

    for name, weight, held in parse_input(s):
        seen.add(name)
        referenced.update(held)
        tree[name] = (weight, held)

    base = list(seen - referenced)
    assert(len(base) == 1)

    base = base[0]

    fixes = {}

    def fix_recursive(name):
        weight, held = tree[name]
        if len(held) == 0:
            return weight

        sub_weights = list(map(fix_recursive, held))

        weight_counts = collections.Counter(sub_weights)
        counts = weight_counts.most_common()
        if len(counts) != 1:
            assert(len(counts) == 2)
            good_weight = counts[0][0]
            bad_weight = counts[1][0]
            assert(counts[1][1] == 1)
            idx = sub_weights.index(bad_weight)
            diff = good_weight - bad_weight
            changed_node = held[idx]
            fixes[changed_node] = tree[changed_node][0] + diff
            sub_weights[idx] = good_weight

        this_weight = weight + sum(sub_weights)
        return this_weight

    fix_recursive(base)

    assert(len(fixes) == 1)

    answer = list(fixes.values())[0]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 7)
part1(INPUT)
part2(INPUT)
