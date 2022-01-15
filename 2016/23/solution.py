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

def run_code(instructions, registers):
    def get_val(val):
        if isinstance(val, str):
            val = registers[val]
        return val

    idx = 0
    while idx < len(instructions):
        inst = instructions[idx]

        if idx + 5 < len(instructions):
            if (instructions[idx][0] == 'cpy' and
                instructions[idx+1][0] == 'inc' and
                instructions[idx+2][0] == 'dec' and
                instructions[idx+3][0] == 'jnz' and
                instructions[idx+4][0] == 'dec' and
                instructions[idx+5][0] == 'jnz' and
                instructions[idx+3][2] == -2 and
                instructions[idx+5][2] == -5 and
                instructions[idx][2] == instructions[idx+2][1] and
                instructions[idx][2] == instructions[idx+3][1] and
                instructions[idx+4][1] == instructions[idx+5][1]):
                # This *seems* to be a multiplication loop
                dst = instructions[idx+1][1]
                cpy_src = instructions[idx][1]
                cpy_dst = instructions[idx+2][1]
                factor = instructions[idx+4][1]
                if (dst not in (cpy_src, cpy_dst, factor) and
                    cpy_src not in (cpy_dst, factor) and
                    cpy_dst != factor):
                    registers[dst] += get_val(cpy_src) * registers[factor]
                    registers[cpy_dst] = 0
                    registers[factor] = 0
                    idx += 6
                    continue

        if inst[0] == 'jnz':
            if get_val(inst[1]) != 0:
                idx += get_val(inst[2])
            else:
                idx += 1
            continue

        if inst[0] == 'inc':
            registers[inst[1]] += 1
        elif inst[0] == 'dec':
            registers[inst[1]] -= 1
        elif inst[0] == 'cpy':
            if inst[2] in 'abcd':
                # Only process if valid
                registers[inst[2]] = get_val(inst[1])
        elif inst[0] == 'tgl':
            offset = get_val(inst[1])
            mod_idx = idx + offset
            if mod_idx < len(instructions):
                if len(instructions[mod_idx]) == 2:
                    # One instruction
                    if instructions[mod_idx][0] == 'inc':
                        instructions[mod_idx][0] = 'dec'
                    else:
                        instructions[mod_idx][0] = 'inc'
                else:
                    # Two instructions
                    if instructions[mod_idx][0] == 'jnz':
                        instructions[mod_idx][0] = 'cpy'
                    else:
                        instructions[mod_idx][0] = 'jnz'
        else:
            assert(False)
        idx += 1

    return registers

def solve(s, init_a):
    registers = {
        name: 0
        for name in 'abcd'
    }
    registers['a'] = init_a

    run_code(parse_instructions(s), registers)

    return registers['a']

def part1(s):
    answer = solve(s, 7)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 12)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 23)
part1(INPUT)
part2(INPUT)
