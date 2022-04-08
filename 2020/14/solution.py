import re

import lib.aoc

def parse_program(prog):
    for line in prog.splitlines():
        m = re.fullmatch('mask = ([X01]+)', line)
        if m is not None:
            yield 'mask', m.group(1)
            continue
        m = re.fullmatch('mem\[(\d+)\] = (\d+)', line)
        if m is not None:
            yield 'mem', int(m.group(1)), int(m.group(2))
            continue
        assert(False)

def part1(s):
    mask = ''
    memory = {}
    for op in parse_program(s):
        if op[0] == 'mask':
            mask = op[1]
        elif op[0] == 'mem':
            _, addr, val = op
            # Apply zeros in mask
            val &= int(mask.replace('X', '1'), 2)
            # Apply ones in mask
            val |= int(mask.replace('X', '0'), 2)
            memory[addr] = val
    answer = sum(memory.values())
    lib.aoc.give_answer(2020, 14, 1, answer)

def all_addresses(addr, addr_mask):
    # Apply ones in mask
    addr |= int(addr_mask.replace('X', '0'), 2)
    candidates = [addr]
    mask = 1
    for c in addr_mask[::-1]:
        if c == 'X':
            candidates = [cand & (~mask) for cand in candidates]
            candidates += [cand | mask for cand in candidates]
        mask <<= 1
    return candidates

def part2(s):
    mask = ''
    memory = {}
    for op in parse_program(s):
        if op[0] == 'mask':
            mask = op[1]
        elif op[0] == 'mem':
            _, addr, val = op
            for a in all_addresses(addr, mask):
                memory[a] = val
    answer = sum(memory.values())
    lib.aoc.give_answer(2020, 14, 2, answer)

INPUT = lib.aoc.get_input(2020, 14)

part1(INPUT)
part2(INPUT)
