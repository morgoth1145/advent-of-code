import re

import helpers.input

def parse_mask(mask):
    to_zero = mask.translate(str.maketrans('X10', '110'))
    to_one = mask.translate(str.maketrans('X10', '010'))
    return int(to_zero, 2), int(to_one, 2)

def part1(s):
    to_zero = 0
    to_one = 0
    memory = {}
    for line in s.splitlines():
        if line.startswith('mask'):
            to_zero, to_one = parse_mask(line.split(' = ')[1])
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

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 14)

part1(INPUT)
part2(INPUT)
