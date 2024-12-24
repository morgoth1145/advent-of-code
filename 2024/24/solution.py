import functools

import lib.aoc

def parse_input(s):
    a, b = s.split('\n\n')

    m = {}
    for line in a.splitlines():
        a0, a1 = line.split(': ')
        m[a0] = int(a1)

    instructions = {}

    for line in b.splitlines():
        left, right = line.split(' -> ')
        parts = left.split()
        instructions[right] = parts

    return m, instructions

def part1(s):
    signals, inst = parse_input(s)

    @functools.cache
    def e(wire):
        if wire in signals:
            return signals[wire]

        left, op, right = inst[wire]
        left = e(left)
        right = e(right)
        if op == 'AND':
            return left & right
        if op == 'OR':
            return left | right
        assert(op == 'XOR')
        return left ^ right

    bits = {}

    for wire in inst:
        if wire.startswith('z'):
            pos = int(wire[1:])
            bits[pos] = e(wire)

    out_bits = [b for _,b in sorted(bits.items(), reverse=True)]
    out_bits = ''.join(map(str, out_bits))

    answer = int(out_bits, base=2)

    lib.aoc.give_answer(2024, 24, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 24)
part1(INPUT)
part2(INPUT)
