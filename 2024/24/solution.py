import functools

import lib.aoc

def parse_input(s):
    a, b = s.split('\n\n')

    signals = {}
    for line in a.splitlines():
        a0, a1 = line.split(': ')
        signals[a0] = int(a1)

    gates = {}

    for line in b.splitlines():
        left, right = line.split(' -> ')
        parts = left.split()
        gates[right] = parts

    return signals, gates

def extract_num(prefix, d):
    bits = {}

    for wire, val in d.items():
        if wire.startswith(prefix):
            pos = int(wire[len(prefix):])
            bits[pos] = val

    out_bits = [b for _,b in sorted(bits.items(), reverse=True)]
    out_bits = ''.join(map(str, out_bits))

    return int(out_bits, base=2)

def run_wires(signals, gates):
    @functools.cache
    def e(wire):
        if wire in signals:
            return signals[wire]

        left, op, right = gates[wire]
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

        for wire in gates:
            if wire.startswith('z'):
                bits[wire] = e(wire)

        return extract_num('z', bits)
    except:
        return None

def part1(s):
    signals, gates = parse_input(s)

    answer = run_wires(signals, gates)

    lib.aoc.give_answer(2024, 24, 1, answer)

def dump_gates_pretty(gates):
    renames = {}

    @functools.cache
    def check_rename(wire):
        if wire not in gates:
            return wire
        if wire.startswith('z'):
            return wire
        left, op, right = gates[wire]
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
        return wire

    for wire in gates:
        check_rename(wire)

    def pad(wire, target_length=20):
        while len(wire) < target_length:
            wire += ' '
        return wire
    @functools.cache
    def dump(wire):
        if wire not in gates:
            return wire
        left, op, right = gates[wire]
        left = dump(left)
        right = dump(right)
        if wire in renames:
            wire = renames[wire]
        print(f'{pad(wire)} = {pad(left)} {pad(op, 5)} {pad(right)}')
        return wire

    num_bits = max(int(s[1:]) for s in gates
                   if s[0] == 'z')

    for i in range(num_bits+1):
        s = 'z' + str(i).zfill(2)
        dump(s)

    print()
    print()
    for old, new in renames.items():
        print(old+'->'+new)
    print()
    print()

def validate_fixed_gates(signals, gates):
    x = extract_num('x', signals)
    y = extract_num('y', signals)

    target = x+y

    assert(run_wires(signals, gates) == target)
    print('Success! The swaps fixed the system, numbers added properly!')

def part2_manual(s):
    signals, gates = parse_input(s)

    swaps = []

    while len(swaps) < 8:
        dump_gates_pretty(gates)
        print('Please analyze and find a pair of wires to swap.')
        first = input('First wire in the swap: ')
        second = input('Second wire in the swap: ')
        gates[first], gates[second] = gates[second], gates[first]
        swaps.append(first)
        swaps.append(second)

    validate_fixed_gates(signals, gates)

    answer = ','.join(sorted(swaps))

    lib.aoc.give_answer(2024, 24, 2, answer)

def part2(s):
    signals, gates = parse_input(s)

    num_bits = max(int(s[1:]) for s in signals)+1

    def find_error():
        # Restart from scratch each time since swapping occurs
        op_to_wire = {}

        xy_xors = {}
        xy_ands = {}
        for wire, (left, op, right) in gates.items():
            op_to_wire[left, op, right] = wire
            if ((left[0] == 'x' and right[0] == 'y') or
                (left[0] == 'y' and right[0] == 'x')):
                assert(left[1:] == right[1:])
                zid = int(left[1:])
                if op == 'XOR':
                    assert(zid not in xy_xors)
                    xy_xors[zid] = wire
                elif op == 'AND':
                    assert(zid not in xy_ands)
                    xy_ands[zid] = wire
                else:
                    assert(False)

        assert(len(xy_xors) == num_bits)
        assert(len(xy_ands) == num_bits)

        z_carry = {}

        for i in range(num_bits+1):
            xid = 'x' + str(i).zfill(2)
            yid = 'y' + str(i).zfill(2)
            zid = 'z' + str(i).zfill(2)
            if i == 0:
                if xy_xors[0] != zid:
                    op_target = (xid, 'XOR', yid)
                    if op_target not in op_to_wire:
                        # It must be reversed!
                        op_target = op_target[::-1]
                    # Fix the first output wire!
                    return zid, op_to_wire[op_target]
                z_carry[0] = xy_ands[0]
            else:
                zout_target = (z_carry[i-1], 'XOR', xy_xors[i])
                if zout_target not in op_to_wire:
                    zout_target = zout_target[::-1]
                if zout_target not in op_to_wire:
                    # We need to swap z_carry[i-1] into the right position!
                    current_left, current_op, current_right = gates[zid]
                    assert(current_op == 'XOR')
                    if current_left == xy_xors[i]:
                        # Left is good, swap the right
                        return current_right, z_carry[i-1]
                    elif current_right == xy_xors[i]:
                        # Right is good, swap the left
                        return current_left, z_carry[i-1]
                    elif current_left == z_carry[i-1]:
                        # Left is good, swap the right
                        return current_right, xy_xors[i]
                    elif current_right == z_carry[i-1]:
                        # Right is good, swap the left
                        return current_left, xy_xors[i]
                    print('Cannot fix this automatically (yet)')
                    assert(False)
                zout = op_to_wire[zout_target]
                if zout != zid:
                    # The output wire is misplaced! Fix it
                    return zid, zout

                carry_and_target = (z_carry[i-1], 'AND', xy_xors[i])
                if carry_and_target not in op_to_wire:
                    carry_and_target = carry_and_target[::-1]
                carry_and = op_to_wire[carry_and_target]

                carry_target = (carry_and, 'OR', xy_ands[i])
                if carry_target not in op_to_wire:
                    carry_target = carry_target[::-1]
                carry = op_to_wire[carry_target]

                z_carry[i] = carry

        return None

    swaps = []
    for i in range(4):
        first, second = find_error()
        print(f'Swapping {first} with {second}...')
        gates[first], gates[second] = gates[second], gates[first]
        swaps += [first, second]

    validate_fixed_gates(signals, gates)

    answer = ','.join(sorted(swaps))

    lib.aoc.give_answer(2024, 24, 2, answer)

INPUT = lib.aoc.get_input(2024, 24)
part1(INPUT)
part2(INPUT)
