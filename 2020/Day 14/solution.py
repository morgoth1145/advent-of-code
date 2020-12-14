import re

import helpers.input

def parse_mask(mask):
    to_zero = mask.translate(str.maketrans('X10', '110'))
    to_one = mask.translate(str.maketrans('X10', '010'))
    floating = mask.translate(str.maketrans('X10', '100'))
    return int(to_zero, 2), int(to_one, 2), int(floating, 2)

def part1(s):
    to_zero = 0
    to_one = 0
    memory = {}
    for line in s.splitlines():
        if line.startswith('mask'):
            to_zero, to_one, _ = parse_mask(line.split(' = ')[1])
            continue
        if line.startswith('mem'):
            m = re.fullmatch('mem\[(\d+)\] = (\d+)', line)
            addr = int(m.group(1))
            val = int(m.group(2))
            val = (val & to_zero) | to_one
            memory[addr] = val
            continue
        assert(False)
    answer = sum(memory.values())
    print(f'The answer to part one is {answer}')

def all_addresses(addr, floating):
    candidates = [addr]
    mask = 1
    while floating > 0:
        if floating & 1:
            new_cands = []
            for c in candidates:
                new_cands.append(c | mask)
                new_cands.append(c & (~mask))
            candidates = new_cands
        mask *= 2
        floating //= 2
    return candidates

def part2(s):
    to_one = 0
    floating = 0
    memory = {}
    for line in s.splitlines():
        if line.startswith('mask'):
            _, to_one, floating = parse_mask(line.split(' = ')[1])
            continue
        if line.startswith('mem'):
            m = re.fullmatch('mem\[(\d+)\] = (\d+)', line)
            addr = int(m.group(1))
            val = int(m.group(2))
            addr = addr | to_one
            for a in all_addresses(addr, floating):
                memory[a] = val
            continue
        assert(False)
    answer = sum(memory.values())
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 14)

part1(INPUT)
part2(INPUT)
