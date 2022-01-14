import lib.aoc

def parse_instructions(s):
    instructions = []

    for line in s.splitlines():
        parts = line.split()
        for i in range(1, len(parts)):
            if parts[i] not in 'abcd':
                parts[i] = int(parts[i])
        instructions.append(parts)

    return instructions

def run_code(instructions):
    registers = {
        name: 0
        for name in 'abcd'
    }

    def get_val(val):
        if isinstance(val, str):
            val = registers[val]
        return val

    idx = 0
    while idx < len(instructions):
        inst = instructions[idx]

        if inst[0] == 'jnz':
            if get_val(inst[1]) != 0:
                idx += inst[2]
            else:
                idx += 1
            continue

        if inst[0] == 'inc':
            registers[inst[1]] += 1
        elif inst[0] == 'dec':
            registers[inst[1]] -= 1
        elif inst[0] == 'cpy':
            registers[inst[2]] = get_val(inst[1])
        else:
            assert(False)
        idx += 1

    return registers

def part1(s):
    instructions = parse_instructions(s)
    registers = run_code(instructions)

    answer = registers['a']

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 12)
part1(INPUT)
part2(INPUT)
