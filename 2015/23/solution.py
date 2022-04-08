import lib.aoc

def run(s, a, b):
    instructions = []

    for line in s.splitlines():
        op, rest = line.split(maxsplit=1)
        rest = rest.split(', ')
        instructions.append((op, rest))

    idx = 0

    while idx < len(instructions):
        op, args = instructions[idx]

        if op == 'jmp':
            idx += int(args[0])
            continue

        val = a if args[0] == 'a' else b

        if op == 'jie':
            if val % 2 == 0:
                idx += int(args[1])
            else:
                idx += 1
            continue
        if op == 'jio':
            if val == 1:
                idx += int(args[1])
            else:
                idx += 1
            continue

        if op == 'hlf':
            val //= 2
        elif op == 'tpl':
            val *= 3
        elif op == 'inc':
            val += 1
        else:
            assert(False)

        if args[0] == 'a':
            a = val
        else:
            b = val

        idx += 1

    return a, b

def part1(s):
    _, answer = run(s, 0, 0)

    lib.aoc.give_answer(2015, 23, 1, answer)

def part2(s):
    _, answer = run(s, 1, 0)

    lib.aoc.give_answer(2015, 23, 2, answer)

INPUT = lib.aoc.get_input(2015, 23)
part1(INPUT)
part2(INPUT)
