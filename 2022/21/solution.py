import operator

import lib.aoc

def parse_monkeys(s):
    barrel = {}
    for line in s.splitlines():
        monkey, rest = line.split(': ')
        rest = rest.split()
        if len(rest) == 1:
            rest = int(rest[0])
        barrel[monkey] = rest
    return barrel

def simplify(barrel, monkey):
    op = barrel[monkey]
    if isinstance(op, int) or isinstance(op, str):
        return op

    a, o, b = op
    a = simplify(barrel, a)
    b = simplify(barrel, b)
    if isinstance(a, int) and isinstance(b, int):
        return {'+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.ifloordiv}[o](a, b)
    return [a, o, b]

def part1(s):
    barrel = parse_monkeys(s)

    answer = simplify(barrel, 'root')

    lib.aoc.give_answer(2022, 21, 1, answer)

def part2(s):
    barrel = parse_monkeys(s)

    barrel['humn'] = 'humn'
    barrel['root'][1] = '=='

    target, _, test = simplify(barrel, 'root')

    if isinstance(test, int):
        target, test = test, target
    else:
        assert(isinstance(target, int))

    while isinstance(test, list):
        a, op, b = test
        if isinstance(a, int):
            if op == '*':
                assert(target % a == 0)
                target //= a
            elif op == '+':
                target -= a
            elif op == '-':
                target = a - target
            else:
                assert(op == '/')
                assert(a % target == 0)
                target = a // target
            test = b
        else:
            assert(isinstance(b, int))
            if op == '*':
                assert(target % b == 0)
                target //= b
            elif op == '+':
                target -= b
            elif op == '-':
                target += b
            else:
                assert(op == '/')
                target *= b
            test = a

    answer = target

    lib.aoc.give_answer(2022, 21, 2, answer)

INPUT = lib.aoc.get_input(2022, 21)
part1(INPUT)
part2(INPUT)
