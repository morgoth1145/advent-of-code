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

INSTRUCTIONS = {}

def addr(regs, a, b, c):
    regs = list(regs)
    if max(a, b, c) > 3:
        return None
    regs[c] = regs[a] + regs[b]
    return regs
INSTRUCTIONS['addr'] = addr

def addi(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = regs[a] + b
    return regs
INSTRUCTIONS['addi'] = addi

def mulr(regs, a, b, c):
    regs = list(regs)
    if max(a, b, c) > 3:
        return None
    regs[c] = regs[a] * regs[b]
    return regs
INSTRUCTIONS['mulr'] = mulr

def muli(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = regs[a] * b
    return regs
INSTRUCTIONS['muli'] = muli

def banr(regs, a, b, c):
    regs = list(regs)
    if max(a, b, c) > 3:
        return None
    regs[c] = regs[a] & regs[b]
    return regs
INSTRUCTIONS['banr'] = banr

def bani(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = regs[a] & b
    return regs
INSTRUCTIONS['bani'] = bani

def borr(regs, a, b, c):
    regs = list(regs)
    if max(a, b, c) > 3:
        return None
    regs[c] = regs[a] | regs[b]
    return regs
INSTRUCTIONS['borr'] = borr

def bori(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = regs[a] | b
    return regs
INSTRUCTIONS['bori'] = bori

def setr(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = regs[a]
    return regs
INSTRUCTIONS['setr'] = setr

def seti(regs, a, b, c):
    regs = list(regs)
    if c > 3:
        return None
    regs[c] = a
    return regs
INSTRUCTIONS['seti'] = seti

def gtir(regs, a, b, c):
    regs = list(regs)
    if max(b, c) > 3:
        return None
    regs[c] = 1 if a > regs[b] else 0
    return regs
INSTRUCTIONS['gtir'] = gtir

def gtri(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = 1 if regs[a] > b else 0
    return regs
INSTRUCTIONS['gtri'] = gtri

def gtrr(regs, a, b, c):
    regs = list(regs)
    if max(a, b, c) > 3:
        return None
    regs[c] = 1 if regs[a] > regs[b] else 0
    return regs
INSTRUCTIONS['gtrr'] = gtrr

def eqir(regs, a, b, c):
    regs = list(regs)
    if max(b, c) > 3:
        return None
    regs[c] = 1 if a == regs[b] else 0
    return regs
INSTRUCTIONS['eqir'] = eqir

def eqri(regs, a, b, c):
    regs = list(regs)
    if max(a, c) > 3:
        return None
    regs[c] = 1 if regs[a] == b else 0
    return regs
INSTRUCTIONS['eqri'] = eqri

def eqrr(regs, a, b, c):
    regs = list(regs)
    if max(a, b, c) > 3:
        return None
    regs[c] = 1 if regs[a] == regs[b] else 0
    return regs
INSTRUCTIONS['eqrr'] = eqrr

def sample_options(before, instruction, after):
    options = set()

    _, a, b, c = instruction

    for name, fn in INSTRUCTIONS.items():
        computed = fn(before, a, b, c)
        if computed is None:
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

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 16)
part1(INPUT)
part2(INPUT)
