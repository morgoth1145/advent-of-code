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

def extract_num(prefix, d):
    bits = {}

    for wire, val in d.items():
        if wire.startswith(prefix):
            pos = int(wire[len(prefix):])
            bits[pos] = val

    out_bits = [b for _,b in sorted(bits.items(), reverse=True)]
    out_bits = ''.join(map(str, out_bits))

    return int(out_bits, base=2)

def run_wires(signals, inst):
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

    try:
        bits = {}

        for wire in inst:
            if wire.startswith('z'):
                bits[wire] = e(wire)

        return extract_num('z', bits)
    except:
        return None

def part1(s):
    signals, inst = parse_input(s)

    answer = run_wires(signals, inst)

    lib.aoc.give_answer(2024, 24, 1, answer)

def dump_instructions(signals, inst):
    renames = {}

    @functools.cache
    def check_rename(wire):
        if wire in signals:
            return wire
        if wire.startswith('z'):
            return wire
        left, op, right = inst[wire]
        if ((left.startswith('x') and right.startswith('y')) or
            left.startswith('y') and right.startswith('x')):
            xid = left[1:]
            yid = right[1:]
            assert(xid == yid)
            new_name = wire
            if op == 'XOR':
                new_name = 'z'+xid+'_xor'
            elif op == 'AND':
                new_name = 'z'+xid+'_and'
            renames[wire] = new_name
            return new_name
        left = check_rename(left)
        right = check_rename(right)
        if (((left[3:] == '_and' and right[3:] == '_xor') or
             (left[3:] == '_xor' and right[3:] == '_and')) and
            op == 'AND'):
            assert(left[0] == 'z' == right[0])
            lid = int(left[1:3])
            rid = int(right[1:3])
            assert(abs(lid-rid) == 1)
            new_name = 'z'+str(max(lid, rid)).zfill(2) + '_carry_and'
            renames[wire] = new_name
            return new_name
        if (((left[3:] == '_carry' and right[3:] == '_xor') or
             (left[3:] == '_xor' and right[3:] == '_carry')) and
            op == 'AND'):
            assert(left[0] == 'z' == right[0])
            lid = int(left[1:3])
            rid = int(right[1:3])
            assert(abs(lid-rid) == 1)
            new_name = 'z'+str(max(lid, rid)).zfill(2) + '_carry_and'
            renames[wire] = new_name
            return new_name
        if (((left[3:] == '_and' and right[3:] == '_carry_and') or
             (left[3:] == '_carry_and' and right[3:] == '_and')) and
            op == 'OR'):
            assert(left[0] == 'z' == right[0])
            lid = int(left[1:3])
            rid = int(right[1:3])
            assert(lid == rid)
            new_name = 'z'+str(lid).zfill(2) + '_carry'
            renames[wire] = new_name
            return new_name
        if (((left[3:] == '_and' and right[3:] == '_carry_and_alt') or
             (left[3:] == '_carry_and_alt' and right[3:] == '_and')) and
            op == 'OR'):
            assert(left[0] == 'z' == right[0])
            lid = int(left[1:3])
            rid = int(right[1:3])
            assert(lid == rid)
            new_name = 'z'+str(lid).zfill(2) + '_carry'
            renames[wire] = new_name
            return new_name
        return wire

    for wire in inst:
        check_rename(wire)

    def pad(wire, target_length=20):
        while len(wire) < target_length:
            wire += ' '
        return wire
    @functools.cache
    def dump(wire):
        if wire in signals:
            return wire
        left, op, right = inst[wire]
        left = dump(left)
        right = dump(right)
        if wire in renames:
            wire = renames[wire]
        print(f'{pad(wire)} = {pad(left)} {pad(op, 5)} {pad(right)}')
        return wire

    num_bits = max(int(s[1:]) for s in signals)+1

    for i in range(num_bits+1):
        s = 'z' + str(i).zfill(2)
        dump(s)

    print()
    print()
    for old, new in renames.items():
        print(old+'->'+new)
    print()
    print()

def part2(s):
    signals, inst = parse_input(s)

    swaps = []

    while len(swaps) < 8:
        dump_instructions(signals, inst)
        print('Please analyze and find a pair of wires to swap.')
        first = input('First wire in the swap: ')
        second = input('Second wire in the swap: ')
        inst[first], inst[second] = inst[second], inst[first]
        swaps.append(first)
        swaps.append(second)

    x = extract_num('x', signals)
    y = extract_num('y', signals)

    target = x+y

    assert(run_wires(signals, inst) == target)
    print('Success! The swaps fixed the system and it added the numbers properly!')

    answer = ','.join(sorted(swaps))

    lib.aoc.give_answer(2024, 24, 2, answer)

INPUT = lib.aoc.get_input(2024, 24)
part1(INPUT)
part2(INPUT)
