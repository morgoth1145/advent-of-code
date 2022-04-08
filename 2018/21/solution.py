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

class QuantumResult:
    def __init__(self, options):
        self.options = options

    def __add__(self, other):
        return QuantumResult([(v+other, test)
                              for v, test in self.options])

class QuantumRegister:
    def __init__(self):
        pass

    def __eq__(self, other):
        return QuantumResult([(1, other), (0, None)])

def bool_to_res(res):
    if isinstance(res, bool):
        return 1 if res else 0
    assert(isinstance(res, QuantumResult))
    return res

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
    'gtir': lambda regs, a, b: bool_to_res(a > regs[b]),
    'gtri': lambda regs, a, b: bool_to_res(regs[a] > b),
    'gtrr': lambda regs, a, b: bool_to_res(regs[a] > regs[b]),
    'eqir': lambda regs, a, b: bool_to_res(a == regs[b]),
    'eqri': lambda regs, a, b: bool_to_res(regs[a] == b),
    'eqrr': lambda regs, a, b: bool_to_res(regs[a] == regs[b]),
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

def gen_solutions_programmatically(s):
    ip_addr, instructions = parse_input(s)
    idx = 0

    assert(all(i[3] != 0
               for i in instructions))

    a_addr = instructions[17][3]
    tmp_addr = instructions[18][3]
    target_addr = instructions[20][2]

    # Floor division block
    assert(0 not in (ip_addr, a_addr, target_addr, tmp_addr))
    assert(len(set((ip_addr, a_addr, target_addr, tmp_addr))) == 4)

    assert(instructions[17] == ['seti', 0, None, a_addr])
    assert(instructions[18] == ['addi', a_addr, 1, tmp_addr])
    assert(instructions[19] == ['muli', tmp_addr, 256, tmp_addr])
    assert(instructions[20] == ['gtrr', tmp_addr, target_addr, tmp_addr])
    assert(instructions[21] in (['addr', ip_addr, tmp_addr, ip_addr],
                                ['addr', tmp_addr, ip_addr, ip_addr]))
    assert(instructions[22] == ['addi', ip_addr, 1, ip_addr])
    assert(instructions[23] == ['seti', 25, None, ip_addr])
    assert(instructions[24] == ['addi', a_addr, 1, a_addr])
    assert(instructions[25] == ['seti', 17, None, ip_addr])

    seen = set()

    regs = [QuantumRegister()] + [0] * 5

    instructions_run = 0

    while idx < len(instructions):
        instructions_run += 1

        if idx == 17:
            # Super instruction
            regs[a_addr] = regs[target_addr] // 256
            regs[tmp_addr] = 1
            idx = 26
            continue

        regs[ip_addr] = idx
        old_regs = list(regs)
        cmd, a, b, c = instructions[idx]
        regs[c] = INSTRUCTIONS[cmd](regs, a, b)
        if isinstance(regs[ip_addr], QuantumResult):
            options = regs[ip_addr].options
            idx_options = []
            for val, test in regs[ip_addr].options:
                if val+1 >= len(instructions):
                    assert(test is not None)
                    if test in seen:
                        return
                    yield test
                    seen.add(test)
                else:
                    idx_options.append(val+1)
            assert(len(idx_options) == 1)
            idx = idx_options[0]
            regs[ip_addr] = idx-1
        else:
            idx = regs[ip_addr] + 1

def part1(s):
    answer = next(gen_solutions_programmatically(s))

    lib.aoc.give_answer(2018, 21, 1, answer)

def part2(s):
    answer = list(gen_solutions_programmatically(s))[-1]

    lib.aoc.give_answer(2018, 21, 2, answer)

INPUT = lib.aoc.get_input(2018, 21)
part1(INPUT)
part2(INPUT)
