import collections
import parse

import lib.aoc

def parse_input(s):
    for group in s.split('\n\n'):
        lines = list(map(str.strip, group.splitlines()))
        n = parse.parse('Monkey {:d}:', lines[0])[0]
        items = list(map(lambda r:r[0], parse.findall('{:d}', lines[1])))
        _, op = lines[2].split(': ')
        assert(op.startswith('new = '))
        op = op.replace('new = ', '')
        divisible_test = parse.parse('Test: divisible by {:d}', lines[3])[0]
        true_dest = parse.parse('If true: throw to monkey {:d}', lines[4])[0]
        false_dest = parse.parse('If false: throw to monkey {:d}', lines[5])[0]

        yield n, items, op, divisible_test, true_dest, false_dest

def run_round(monkey_items, monkey_meta, inspect_counts):
    for n, (op, divisible_test, true_dest, false_dest) in monkey_meta.items():
        items = monkey_items.pop(n, [])
        monkey_items[n] = []
        inspect_counts[n] += len(items)
        for worry in items:
            worry = eval(op, None, {'old': worry})
            worry //= 3
            if worry % divisible_test == 0:
                monkey_items[true_dest].append(worry)
            else:
                monkey_items[false_dest].append(worry)

def part1(s):
    monkeys = list(parse_input(s))

    monkey_items = {n: items
                    for n, items, op, divisible_test, true_dest, false_dest
                    in monkeys}
    monkey_meta = {n: (op, divisible_test, true_dest, false_dest)
                   for n, items, op, divisible_test, true_dest, false_dest
                   in monkeys}
    inspect_counts = collections.Counter()

    for _ in range(20):
        run_round(monkey_items, monkey_meta, inspect_counts)

    most_active = inspect_counts.most_common(2)
    answer = most_active[0][1] * most_active[1][1]

    lib.aoc.give_answer(2022, 11, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 11)
part1(INPUT)
part2(INPUT)
