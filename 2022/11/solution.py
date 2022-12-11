import operator
import math

import lib.aoc

class Monkey:
    def __init__(self, spec):
        lines = list(map(str.strip, spec.splitlines()))
        self.number = int(lines[0].split()[1][:-1])
        self.items = list(map(int, lines[1].split(': ')[1].split(', ')))

        # Parse the operation into lambda functions
        # It's tedious, but runs much faster (and feels better than using eval!)
        left, op, right = lines[2].split('new = ')[1].split()
        assert(left == 'old')
        binary_ops = {'*': operator.mul, '+': operator.add}
        op = binary_ops[op]
        if right == 'old':
            self.op = lambda worry: op(worry, worry)
        else:
            self.op = lambda worry: op(worry, int(right))

        self.divisor = int(lines[3].split()[-1])
        self.true_dest = int(lines[4].split()[-1])
        self.false_dest = int(lines[5].split()[-1])
        self.inspections = 0

    def inspect_items(self, mod_by, div_by):
        inspected = map(self.op, self.items)
        if div_by is not None:
            inspected = [worry // div_by for worry in inspected]
        inspected = [worry % mod_by for worry in inspected]

        self.items = []
        self.inspections += len(inspected)

        for worry in inspected:
            if worry % self.divisor == 0:
                yield worry, self.true_dest
            else:
                yield worry, self.false_dest

def solve(s, rounds, div_by=None):
    monkeys = list(map(Monkey, s.split('\n\n')))
    assert(all(idx == m.number for idx, m in enumerate(monkeys)))

    mod_by = math.lcm(*[m.divisor for m in monkeys])

    for _ in range(rounds):
        for m in monkeys:
            for worry, dest in m.inspect_items(mod_by, div_by):
                monkeys[dest].items.append(worry)

    a, b = sorted(m.inspections for m in monkeys)[-2:]
    return a * b

def part1(s):
    answer = solve(s, 20, div_by=3)

    lib.aoc.give_answer(2022, 11, 1, answer)

def part2(s):
    answer = solve(s, 10000)

    lib.aoc.give_answer(2022, 11, 2, answer)

INPUT = lib.aoc.get_input(2022, 11)
part1(INPUT)
part2(INPUT)
