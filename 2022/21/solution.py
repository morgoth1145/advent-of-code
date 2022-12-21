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
    pass

INPUT = lib.aoc.get_input(2022, 21)
part1(INPUT)
part2(INPUT)
