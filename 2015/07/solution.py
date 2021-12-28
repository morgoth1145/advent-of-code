import functools

import lib.aoc

def parse_input(s):
    wires = {}
    for line in s.splitlines():
        left, right = line.split(' -> ')
        left = left.split()
        wires[right] = left
    return wires

def evaluate_wires(wires, target):
    @functools.cache
    def impl(target):
        try:
            return int(target)
        except:
            pass

        op = wires[target]
        if 1 == len(op):
            return impl(op[0])

        if 2 == len(op):
            NOT, other = op
            assert(NOT == 'NOT')
            return 0xFFFF ^ impl(other)

        left, op, right = op
        left = impl(left)
        right = impl(right)

        if op == 'AND':
            return left & right
        elif op == 'OR':
            return left | right
        elif op == 'LSHIFT':
            return left << right
        elif op == 'RSHIFT':
            return left >> right
        else:
            assert(False)

    return impl(target)

def part1(s):
    wires = parse_input(s)

    answer = evaluate_wires(wires, 'a')

    print(f'The answer to part one is {answer}')

def part2(s):
    wires = parse_input(s)
    wires['b'] = [evaluate_wires(wires, 'a')]

    answer = evaluate_wires(wires, 'a')

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 7)
part1(INPUT)
part2(INPUT)
