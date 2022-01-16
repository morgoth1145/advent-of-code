import collections

import lib.aoc

def parse_tree(s):
    tree = {}
    referenced = set()

    for line in s.splitlines():
        parts = line.split(' -> ')
        name, weight = parts[0].split()
        assert(weight[0] == '(' and weight[-1] == ')')
        weight = int(weight[1:-1])
        if len(parts) == 2:
            held = parts[1].split(', ')
        else:
            held = []
        tree[name] = (weight, held)
        referenced.update(held)

    root = set(tree.keys()) - referenced
    assert(len(root) == 1)
    return list(root)[0], tree

def part1(s):
    answer, _ = parse_tree(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    root, tree = parse_tree(s)

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

    fix_recursive(root)

    assert(len(fixes) == 1)

    answer = list(fixes.values())[0]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 7)
part1(INPUT)
part2(INPUT)
