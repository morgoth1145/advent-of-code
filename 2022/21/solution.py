import lib.aoc

def parse_monkeys(s):
    barrel = {}
    for line in s.splitlines():
        monkey, rest = line.split(': ')
        if all(c.isdigit() for c in rest):
            rest = int(rest)
        else:
            rest = rest.split()
        barrel[monkey] = rest
    return barrel

def part1(s):
    barrel = parse_monkeys(s)

    def yells(monkey):
        op = barrel[monkey]
        if isinstance(op, int):
            return op

        a, o, b = op
        if o == '/':
            o = '//'
        a = yells(a)
        b = yells(b)
        return eval(f'{a} {o} {b}')

    answer = yells('root')

    lib.aoc.give_answer(2022, 21, 1, answer)

def part2(s):
    barrel = parse_monkeys(s)

    def yells(monkey):
        if monkey == 'humn':
            return 'humn'
        op = barrel[monkey]
        if isinstance(op, int):
            return op

        a, o, b = op
        if monkey == 'root':
            o = '=='
        if o == '/':
            o = '//'
        a = yells(a)
        b = yells(b)
        if isinstance(a, int) and isinstance(b, int):
            return eval(f'{a} {o} {b}')
        return [a, o, b]

    test = yells('root')

    assert('==' == test[1])

    a, _, b = test

    if isinstance(a, int):
        target = a
        test = b
    else:
        assert(isinstance(b, int))
        target = b
        test = a

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
            elif op == '//':
                assert(a % target == 0)
                target = a // target
            else:
                print('a', op)
                assert(False)
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
            elif op == '//':
                target *= b
            else:
                print('b', op)
                assert(False)
            test = a

    answer = target

    lib.aoc.give_answer(2022, 21, 2, answer)

INPUT = lib.aoc.get_input(2022, 21)
part1(INPUT)
part2(INPUT)
