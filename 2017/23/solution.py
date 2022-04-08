import lib.aoc

def part1(s):
    registers = {r:0
                 for r in 'abcdefgh'}

    def get_val(v):
        if v in 'abcdefgh':
            return registers[v]
        return int(v)

    instructions = [l.split()
                    for l in s.splitlines()]

    idx = 0
    answer = 0

    while idx < len(instructions):
        cmd, arg1, arg2 = instructions[idx]

        if cmd == 'jnz':
            if get_val(arg1) != 0:
                idx += get_val(arg2)
                continue
        elif cmd == 'set':
            registers[arg1] = get_val(arg2)
        elif cmd == 'sub':
            registers[arg1] -= get_val(arg2)
        elif cmd == 'mul':
            answer += 1
            registers[arg1] *= get_val(arg2)
        else:
            assert(False)

        idx += 1

    lib.aoc.give_answer(2017, 23, 1, answer)

def part2_reverse_engineer(s):
    jump_points = set()

    instructions = [l.split()
                    for l in s.splitlines()]

    translated = []

    for idx, (cmd, arg1, arg2) in enumerate(instructions):
        if cmd == 'set':
            translated.append(f'{arg1} = {arg2}')
        elif cmd == 'sub':
            translated.append(f'{arg1} -= {arg2}')
        elif cmd == 'mul':
            translated.append(f'{arg1} *= {arg2}')
        elif cmd == 'jnz':
            offset = int(arg2)
            dest = idx + offset
            jump_points.add(dest)
            translated.append(f'if {arg1} != 0:\n        GOTO LABEL{dest}')
        else:
            assert(False)

    for idx, cmd in enumerate(translated):
        if idx in jump_points:
            jump_points.remove(idx)
            print(f'LABEL{idx}:')
        print(f'    {cmd}')

    for idx in sorted(jump_points):
        print(f'LABEL{idx}:')

    print('Please reverse-engineer the code and find the answer')
    answer = input('Answer? ')

    lib.aoc.give_answer(2017, 23, 2, answer)

def part2_general(s):
    registers = {r:0
                 for r in 'bcdefgh'}
    registers['a'] = 1

    def get_val(v):
        if v in 'abcdefgh':
            return registers[v]
        return int(v)

    inst = [l.split() for l in s.splitlines()]

    idx = 0

    while idx < len(inst):
        cmd, arg1, arg2 = inst[idx]

        if idx+8 < len(inst):
            # Check for pattern
            # set g d
            # mul g e
            # sub g b
            # jnz g 2
            # set f 0
            # sub e -1
            # set g e
            # sub g b
            # jnz g -8
            if (cmd == 'set' and
                inst[idx+1][0] == 'mul' and
                inst[idx+2][0] == 'sub' and
                inst[idx+3][0] == 'jnz' and
                inst[idx+4][0] == 'set' and
                inst[idx+5][0] == 'sub' and
                inst[idx+6][0] == 'set' and
                inst[idx+7][0] == 'sub' and
                inst[idx+8][0] == 'jnz' and
                # Jumps
                inst[idx+3][2] == '2' and
                inst[idx+5][2] == '-1' and
                inst[idx+8][2] == '-8' and
                # g
                arg1 == inst[idx+1][1] and
                arg1 == inst[idx+2][1] and
                arg1 == inst[idx+3][1] and
                arg1 == inst[idx+6][1] and
                arg1 == inst[idx+7][1] and
                arg1 == inst[idx+8][1] and
                # Whatever we set f to must be a constant
                inst[idx+4][2] not in 'abcdefgh' and
                # e
                inst[idx+1][2] == inst[idx+5][1] and
                inst[idx+1][2] == inst[idx+6][2] and
                # b
                inst[idx+2][2] == inst[idx+7][2] and
                # All variables must be unique
                len(set(arg1+arg2+inst[idx+1][2]+inst[idx+2][2]+inst[idx+4][1])) == 5
                ):
                # Equivalent to
                # if d * e <= b:
                #     if b % d == 0:
                #         f = 0
                # e = b
                # g = 0
##                assert(False)
                d = get_val(arg2)
                e = get_val(inst[idx+1][2])
                b = get_val(inst[idx+2][2])
                if d * e <= b:
                    if b % d == 0:
                        registers[inst[idx+4][1]] = int(inst[idx+4][2])
                registers[inst[idx+1][2]] = b
                registers[arg1] = 0
                idx += 9
                continue

        if cmd == 'jnz':
            if get_val(arg1) != 0:
                idx += get_val(arg2)
                continue
        elif cmd == 'set':
            registers[arg1] = get_val(arg2)
        elif cmd == 'sub':
            registers[arg1] -= get_val(arg2)
        elif cmd == 'mul':
            registers[arg1] *= get_val(arg2)
        else:
            assert(False)

        idx += 1

    answer = registers['h']

    lib.aoc.give_answer(2017, 23, 2, answer)

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d*d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def part2_hardcoded(s):
    answer = 0

    inst = [l.split() for l in s.splitlines()]
    assert(len(inst) == 32)

    low = int(inst[0][2]) * int(inst[4][2]) - int(inst[5][2])
    high = low - int(inst[7][2])
    step = -int(inst[30][2])

    for n in range(low, high+1, step):
        if not is_prime(n):
            answer += 1

    lib.aoc.give_answer(2017, 23, 2, answer)

##part2 = part2_reverse_engineer
##part2 = part2_general
part2 = part2_hardcoded

INPUT = lib.aoc.get_input(2017, 23)
part1(INPUT)
part2(INPUT)
