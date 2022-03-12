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
    pass

INPUT = lib.aoc.get_input(2017, 23)
part1(INPUT)
part2(INPUT)
