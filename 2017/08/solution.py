import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        var1, op, val, _, var2, cond, target = line.split()
        val = int(val)
        target = int(target)
        yield var1, op, val, var2, cond, target

CONDITIONS = {
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
}

OPERATIONS = {
    'inc': lambda a, b: a + b,
    'dec': lambda a, b: a - b,
}

def part1(s):
    registers = {}

    for var1, op, val, var2, cond, target in parse_input(s):
        if CONDITIONS[cond](registers.get(var2, 0), target):
            val = OPERATIONS[op](registers.get(var1, 0), val)
            registers[var1] = val

    answer = max(registers.values())

    print(f'The answer to part one is {answer}')

def part2(s):
    registers = {}

    answer = 0

    for var1, op, val, var2, cond, target in parse_input(s):
        if CONDITIONS[cond](registers.get(var2, 0), target):
            val = OPERATIONS[op](registers.get(var1, 0), val)
            answer = max(answer, val)
            registers[var1] = val

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 8)
part1(INPUT)
part2(INPUT)
