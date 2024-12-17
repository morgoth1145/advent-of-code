import lib.aoc

def parse_prog(s):
    registers, prog = s.split('\n\n')

    registers = list(int(l.split(': ')[1])
                     for l in registers.splitlines())
    prog = list(map(int, prog.split(': ')[1].split(',')))

    return registers, prog

def exec_prog(prog, a, b, c):
    ip = 0

    out = []

    while ip < len(prog):
        def combo(operand):
            if 0 <= operand <= 3:
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
            a = a >> combo(operand)
        elif opcode == 1:
            # bxl
            b = b ^ operand
        elif opcode == 2:
            # bst
            b = combo(operand) % 8
        elif opcode == 3:
            # jnz
            if a != 0:
                ip = operand
                continue
        elif opcode == 4:
            # bxc
            b = b ^ c
        elif opcode == 5:
            # out
            out.append(combo(operand) % 8)
        elif opcode == 6:
            # bdv
            b = a >> combo(operand)
        elif opcode == 7:
            # cdv
            c = a >> combo(operand)

        ip += 2

    return out

def part1(s):
    registers, prog = parse_prog(s)
    answer = ','.join(map(str, exec_prog(prog, *registers)))

    lib.aoc.give_answer(2024, 17, 1, answer)

def part2(s):
    _, prog = parse_prog(s)

    # Assume that the program is structured to loop until a is 0
    # Also assume that a is consumed 3 bits at a time

    candidates = [0]

    expected = []

    for target in prog[::-1]:
        expected.insert(0, target)

        valid = []

        for a in candidates:
            for a_cand in range(a*8, a*8+8):
                if exec_prog(prog, a_cand, 0, 0) == expected:
                    valid.append(a_cand)

        assert(len(valid) > 0)
        candidates = valid

    answer = min(candidates)

    lib.aoc.give_answer(2024, 17, 2, answer)

INPUT = lib.aoc.get_input(2024, 17)
part1(INPUT)
part2(INPUT)
