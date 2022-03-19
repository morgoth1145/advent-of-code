import lib.aoc

def parse_input(s):
    ip_addr, *instructions = s.splitlines()
    ip_addr = int(ip_addr.split()[1])
    instructions = [i.split() for i in instructions]
    instructions = [[cmd, int(a), int(b), int(c)]
                    for cmd, a, b, c in instructions]
    for i in instructions:
        if i[0] in ('seti', 'setr'):
            i[2] = None # Unused argument

    return ip_addr, instructions

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

def trace_sim(s, reg0, num_to_run):
    ip_addr, instructions = parse_input(s)
    idx = 0

    regs = [reg0] + [0] * 5

    instructions_run = 0

    while idx < len(instructions):
        regs[ip_addr] = idx
        old_regs = list(regs)
        cmd, a, b, c = instructions[idx]
        regs[c] = INSTRUCTIONS[cmd](regs, a, b)
        print(f'ip={idx}', old_regs, cmd, a, b, c, regs)
        instructions_run += 1
        if instructions_run >= num_to_run:
            assert(False)
        idx = regs[ip_addr] + 1

def solve_decompiled(s, reg0):
    INSTRUCTIONS_AS_STRING = {
        'addr': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] + regs[{b}]'),
        'addi': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] + {b}'),
        'mulr': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] * regs[{b}]'),
        'muli': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] * {b}'),
        'banr': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] & regs[{b}]'),
        'bani': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] & {b}'),
        'borr': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] | regs[{b}]'),
        'bori': lambda a, b, c: (f'regs[{c}]', f'regs[{a}] | {b}'),
        'setr': lambda a, b, c: (f'regs[{c}]', f'regs[{a}]'),
        'seti': lambda a, b, c: (f'regs[{c}]', f'{a}'),
        'gtir': lambda a, b, c: (f'regs[{c}]', f'1 if {a} > regs[{b}] else 0'),
        'gtri': lambda a, b, c: (f'regs[{c}]', f'1 if regs[{a}] > {b} else 0'),
        'gtrr': lambda a, b, c: (f'regs[{c}]', f'1 if regs[{a}] > regs[{b}] else 0'),
        'eqir': lambda a, b, c: (f'regs[{c}]', f'1 if {a} == regs[{b}] else 0'),
        'eqri': lambda a, b, c: (f'regs[{c}]', f'1 if regs[{a}] == {b} else 0'),
        'eqrr': lambda a, b, c: (f'regs[{c}]', f'1 if regs[{a}] == regs[{b}] else 0'),
    }

    ip_addr, instructions = parse_input(s)

    assert(ip_addr != 0)

    regs = [reg0] + [0] * 5

    print('idx = 0')
    print(f'regs = {regs}')
    print()
    print('while (true)')
    print('{')
    print('    switch (idx)')
    print('    {')
    for inst_idx, (cmd, a, b, c) in enumerate(instructions):
        print(f'    case {inst_idx}:')
        lhs, rhs = INSTRUCTIONS_AS_STRING[cmd](a, b, c)
        if ip_addr in (a, b):
            rhs = rhs.replace(f'regs[{ip_addr}]', str(inst_idx))
        if c == ip_addr:
            print(f'        idx = {rhs} + 1')
            print('        break;')
        else:
            print(f'        {lhs} = {rhs}')
            assert(inst_idx+1 < len(instructions))
    print('    default:')
    print('        return;')
    print('    }')
    print('}')

    print('Please decompile, human')
    return int(input('What is the answer? '))

def part1(s):
    print('What value of reg[0] will halt in the least instructions?')
    answer = solve_decompiled(s, 0)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 21)
part1(INPUT)
part2(INPUT)
