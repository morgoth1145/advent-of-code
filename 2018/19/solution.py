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

def solve_sim(s, reg0):
    ip_addr, instructions = parse_input(s)
    idx = 0

    regs = [reg0] + [0] * 5

    while idx < len(instructions):
        regs[ip_addr] = idx
        cmd, a, b, c = instructions[idx]
        regs[c] = INSTRUCTIONS[cmd](regs, a, b)
        idx = regs[ip_addr] + 1

    return regs[0]

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
    print('        return regs[0];')
    print('    }')
    print('}')

    print('Please decompile, human')
    return int(input('What is the answer? '))

def solve_optimized_sim(s, reg0):
    ip_addr, instructions = parse_input(s)
    idx = 0

    out_addr = 0
    a_addr = instructions[3][1]
    b_addr = instructions[2][3]
    tmp_addr = instructions[3][3]
    target_addr = instructions[4][2]
    assert(sorted([out_addr, ip_addr, tmp_addr,
                   target_addr, a_addr, b_addr]) == list(range(6)))

    assert(instructions[2] == ['seti', 1, None, b_addr])
    assert(instructions[3] in (['mulr', a_addr, b_addr, tmp_addr],
                               ['mulr', b_addr, a_addr, tmp_addr]))
    assert(instructions[4] in (['eqrr', tmp_addr, target_addr, tmp_addr],
                               ['eqrr', target_addr, tmp_addr, tmp_addr]))
    assert(instructions[5] in (['addr', ip_addr, tmp_addr, ip_addr],
                               ['addr', tmp_addr, ip_addr, ip_addr]))
    assert(instructions[6] == ['addi', ip_addr, 1, ip_addr])
    assert(instructions[7] in (['addr', out_addr, a_addr, out_addr],
                               ['addr', a_addr, out_addr, out_addr]))
    assert(instructions[8] == ['addi', b_addr, 1, b_addr])
    assert(instructions[9] == ['gtrr', b_addr, target_addr, tmp_addr])
    assert(instructions[10] in (['addr', ip_addr, tmp_addr, ip_addr],
                                ['addr', tmp_addr, ip_addr, ip_addr]))
    assert(instructions[11] == ['seti', 2, None, ip_addr])

    regs = [reg0] + [0] * 5

    while idx < len(instructions):
        if idx == 2:
            if regs[target_addr] % regs[a_addr] == 0:
                regs[out_addr] += regs[a_addr]
            regs[tmp_addr] = 0
            regs[b_addr] == regs[target_addr]+1
            regs[ip_addr] = 11
            idx = 12
            continue

        regs[ip_addr] = idx
        cmd, a, b, c = instructions[idx]
        regs[c] = INSTRUCTIONS[cmd](regs, a, b)
        idx = regs[ip_addr] + 1

    return regs[0]

def part1(s):
    answer = solve_optimized_sim(s, 0)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve_optimized_sim(s, 1)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 19)
part1(INPUT)
part2(INPUT)
