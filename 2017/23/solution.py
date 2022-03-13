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

    print(f'The answer to part one is {answer}')

def part2(s):
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
            translated.append(f'if {arg1} != 0: GOTO LABEL{dest}')
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

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 23)
part1(INPUT)
part2(INPUT)
