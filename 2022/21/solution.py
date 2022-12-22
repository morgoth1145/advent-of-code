import sympy

import lib.aoc

def parse_monkeys(s):
    barrel = {}
    for line in s.splitlines():
        monkey, job = line.split(': ')
        barrel[monkey] = job
    return barrel

def to_expr(barrel, monkey):
    job = barrel[monkey].split()
    if len(job) == 1:
        return job[0]
    left, op, right = job
    return f'({to_expr(barrel, left)}) {op} ({to_expr(barrel, right)})'

def part1(s):
    answer = sympy.parse_expr(to_expr(parse_monkeys(s), 'root'))

    lib.aoc.give_answer(2022, 21, 1, answer)

def part2(s):
    barrel = parse_monkeys(s)

    barrel['humn'] = 'humn'
    left, _, right = barrel['root'].split()

    left = sympy.parse_expr(to_expr(barrel, left))
    right = sympy.parse_expr(to_expr(barrel, right))

    answer = sympy.solve(sympy.Eq(left, right))[0]

    lib.aoc.give_answer(2022, 21, 2, answer)

INPUT = lib.aoc.get_input(2022, 21)
part1(INPUT)
part2(INPUT)
