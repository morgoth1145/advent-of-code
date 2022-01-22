import lib.aoc

def parse_instructions(s):
    instructions = []

    for line in s.splitlines():
        parts = line.split()
        if parts[-1] not in 'abcdefghijklmnopqrstuvwxyz':
            parts[-1] = int(parts[-1])
        instructions.append(parts)

    return instructions

def part1(s):
    instructions = parse_instructions(s)

    idx = 0
    registers = {}
    last_frequency = None

    def get_val(val):
        if isinstance(val, int):
            return val
        return registers.get(val, 0)

    while True:
        inst = instructions[idx]

        if inst[0] == 'snd':
            last_frequency = get_val(inst[1])
        elif inst[0] == 'set':
            registers[inst[1]] = get_val(inst[2])
        elif inst[0] == 'add':
            registers[inst[1]] = get_val(inst[1]) + get_val(inst[2])
        elif inst[0] == 'mul':
            registers[inst[1]] = get_val(inst[1]) * get_val(inst[2])
        elif inst[0] == 'mod':
            registers[inst[1]] = get_val(inst[1]) % get_val(inst[2])
        elif inst[0] == 'rcv':
            x = get_val(inst[1])
            if x:
                answer = last_frequency
                break
        elif inst[0] == 'jgz':
            if get_val(inst[1]):
                idx += get_val(inst[2])
                continue
        else:
            assert(False)

        idx += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 18)
part1(INPUT)
part2(INPUT)
