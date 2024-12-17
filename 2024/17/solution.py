import lib.aoc

def parse_input(s):
    registers, prog = s.split('\n\n')

    prog = tuple(map(int, prog.split(': ')[1].split(',')))
    a, b, c = tuple(int(l.split(': ')[1])
                    for l in registers.splitlines())

    return (a, b, c), prog

def part1(s):
    (a, b, c), prog = parse_input(s)

    ip = 0

    out = []

    while ip < len(prog):
        def combo(operand):
            if operand in (0, 1, 2, 3):
                return operand
            if operand == 4:
                return a
            if operand == 5:
                return b
            if operand == 6:
                return c
            assert(False)

        opcode = prog[ip]
        operand = prog[ip+1]

        if opcode == 0:
            # adv
            res = a // (2**combo(operand))
            a = res
            ip += 2
            continue

        if opcode == 1:
            # bxl
            res = b ^ operand
            b = res
            ip += 2
            continue

        if opcode == 2:
            # bst
            b = combo(operand) % 8
            ip += 2
            continue

        if opcode == 3:
            # jnz
            if a == 0:
                ip += 2
            else:
                ip = operand
            continue

        if opcode == 4:
            # bxc
            b = b ^ c
            ip += 2
            continue

        if opcode == 5:
            # out
            out.append(combo(operand) % 8)
            ip += 2
            continue

        if opcode == 6:
            # bdv
            res = a // (2**combo(operand))
            b = res
            ip += 2
            continue

        if opcode == 7:
            # cdv
            res = a // (2**combo(operand))
            c = res
            ip += 2
            continue

    answer = ','.join(map(str, out))

    lib.aoc.give_answer(2024, 17, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 17)
part1(INPUT)
part2(INPUT)
