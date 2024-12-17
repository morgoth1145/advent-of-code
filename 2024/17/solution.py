import lib.aoc

def parse_input(s):
    registers, prog = s.split('\n\n')

    prog = tuple(map(int, prog.split(': ')[1].split(',')))
    a, b, c = tuple(int(l.split(': ')[1])
                    for l in registers.splitlines())

    return (a, b, c), prog

def run_prog(a, b, c, prog):
    prog = prog[:]

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

    return out

def part1(s):
    (a, b, c), prog = parse_input(s)

    out = run_prog(a, b, c, prog)
    answer = ','.join(map(str, out))

    lib.aoc.give_answer(2024, 17, 1, answer)

def solve_manual(s):
    _, prog = parse_input(s)

    def combo(operand):
        if operand in (0, 1, 2, 3):
            return str(operand)
        if operand == 4:
            return 'a'
        if operand == 5:
            return 'b'
        if operand == 6:
            return 'c'
        print(f'Bad combo operand {operand}!')
        assert(False)

    print('a = 0')
    print('b = 0')
    print('c = 0')
    print()

    ip = 0

    for ip in range(0, len(prog), 2):
        print(f'LABEL{ip}:')

        opcode = prog[ip]
        operand = prog[ip+1]

        if opcode == 0:
            # adv
            print(f'    a = a // (2 ** {combo(operand)})')
            continue

        if opcode == 1:
            # bxl
            print(f'    b = b ^ {operand}')
            continue

        if opcode == 2:
            # bst
            print(f'    b = {combo(operand)} % 8')
            continue

        if opcode == 3:
            # jnz
            print('    if a != 0:')
            print(f'        goto LABEL{operand}')
            continue

        if opcode == 4:
            # bxc
            print(f'    b = b ^ c')
            continue

        if opcode == 5:
            # out
            print(f'    out.append({combo(operand)} % 8)')
            continue

        if opcode == 6:
            # bdv
            print(f'    b = a // (2 ** {combo(operand)})')
            continue

        if opcode == 7:
            # cdv
            print(f'    c = a // (2 ** {combo(operand)})')
            continue

    answer = int(input('Please decompile, analyze, and give the answer: '))

    assert(list(run_prog(answer, 0, 0, prog)) == list(prog))
    return answer

def part2(s):
    answer = solve_manual(s)

    lib.aoc.give_answer(2024, 17, 2, answer)

INPUT = lib.aoc.get_input(2024, 17)
part1(INPUT)
part2(INPUT)
