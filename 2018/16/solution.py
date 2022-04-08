import json

import lib.aoc

def parse_input(s):
    a, b = s.split('\n\n\n\n')

    samples = []
    for g in a.split('\n\n'):
        lines = g.splitlines()
        before = json.loads(lines[0].replace('Before: ', ''))
        instruction = list(map(int, lines[1].split()))
        after = json.loads(lines[2].replace('After: ', ''))

        samples.append((before, instruction, after))

    program = []
    for line in b.splitlines():
        program.append(list(map(int, line.split())))

    return samples, program

INSTRUCTIONS = {
    'addr': lambda regs, a, b: regs[a] + regs[b],
    'addi': lambda regs, a, b: regs[a] + b,
    'mulr': lambda regs, a, b: regs[a] * regs[b],
    'muli': lambda regs, a, b: regs[a] * b,
    'banr': lambda regs, a, b: regs[a] & regs[b],
    'bani': lambda regs, a, b: regs[a] & b,
    'borr': lambda regs, a, b: regs[a] | regs[b],
    'bori': lambda regs, a, b: regs[a] | b,
    'setr': lambda regs, a, b: regs[a],
    'seti': lambda regs, a, b: a,
    'gtir': lambda regs, a, b: 1 if a > regs[b] else 0,
    'gtri': lambda regs, a, b: 1 if regs[a] > b else 0,
    'gtrr': lambda regs, a, b: 1 if regs[a] > regs[b] else 0,
    'eqir': lambda regs, a, b: 1 if a == regs[b] else 0,
    'eqri': lambda regs, a, b: 1 if regs[a] == b else 0,
    'eqrr': lambda regs, a, b: 1 if regs[a] == regs[b] else 0,
}

def sample_options(before, instruction, after):
    options = set()

    _, a, b, c = instruction

    for name, fn in INSTRUCTIONS.items():
        computed = list(before)
        try:
            computed[c] = fn(computed, a, b)
        except:
            # Register lookup failed
            continue
        if computed != after:
            continue

        options.add(name)

    assert(len(options) > 0)
    return options

def part1(s):
    samples, program = parse_input(s)

    answer = 0
    for before, instruction, after in samples:
        if len(sample_options(before, instruction, after)) >= 3:
            answer += 1

    lib.aoc.give_answer(2018, 16, 1, answer)

def part2(s):
    samples, program = parse_input(s)

    opcode_options = {
        code: set(INSTRUCTIONS.keys())
        for code in range(16)
    }

    for before, instruction, after in samples:
        opcode = instruction[0]
        opcode_options[opcode] &= sample_options(before, instruction, after)

    deduced = {}
    while opcode_options:
        new_known = []
        new_assigned = set()

        for code, options in opcode_options.items():
            if len(options) == 1:
                name = list(options)[0]
                new_known.append(code)
                new_assigned.add(name)
                deduced[code] = name

        for code in new_known:
            del opcode_options[code]

        for code, options in opcode_options.items():
            opcode_options[code] = options - new_assigned

    registers = [0] * 4

    for opcode, a, b, c in program:
        name = deduced[opcode]
        registers[c] = INSTRUCTIONS[name](registers, a, b)

    answer = registers[0]

    lib.aoc.give_answer(2018, 16, 2, answer)

INPUT = lib.aoc.get_input(2018, 16)
part1(INPUT)
part2(INPUT)
