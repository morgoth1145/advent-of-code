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
            registers[inst[2]] = get_val(inst[1])
        elif inst[0] == 'out':
            yield get_val(inst[1])
        else:
            assert(False)
        idx += 1

def part1(s):
    instructions = list(parse_instructions(s))

    answer = 0
    while True:
        registers = {
            name: 0
            for name in 'abcd'
        }
        registers['a'] = answer

        gen = run_code(instructions, registers)

        valid = True
        # Assume if it matches this much that it matches forever
        for val in (0, 1) * 10:
            if next(gen) != val:
                valid = False
                break

        if valid:
            break

        answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2016, 25)
part1(INPUT)
part2(INPUT)
