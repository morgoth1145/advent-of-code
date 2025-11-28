import collections
import functools

import lib.aoc
import lib.graph

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

def validate_fixed_gates(signals, gates):
    x = extract_num('x', signals)
    y = extract_num('y', signals)

    target = x+y

    assert(run_wires(signals, gates) == target)
    print('Success! The swaps fixed the system, numbers added properly!')

def part2_manual(s):
    signals, gates = parse_input(s)

    def plot_graph():
        # Rename wires to include the gate type. This keeps the generated
        # graph smaller and easier to parse visually.
        renaming = {}
        for wire, (_, op, _) in gates.items():
            renaming[wire] = wire + ': ' + op

        graph = collections.defaultdict(list)

        c = collections.Counter()

        coloring = {}

        for wire, (left, op, right) in gates.items():
            left = renaming.get(left, left)
            right = renaming.get(right, right)
            wire = renaming.get(wire, wire)

            graph[left].append(wire)
            graph[right].append(wire)

            color = {'XOR': 'blue',
                     'AND': 'red',
                     'OR': 'green'}[op]
            coloring[wire] = color

        lib.graph.plot_graph(graph, distance=False, coloring=coloring,
                             fix_nodes_after_dragging=True)

    swaps = []

    for _ in range(4):
        plot_graph()

        print('Please analyze and find a pair of wires to swap.')
        first = input('First wire in the swap: ')
        second = input('Second wire in the swap: ')
        gates[first], gates[second] = gates[second], gates[first]
        swaps.append(first)
        swaps.append(second)

    validate_fixed_gates(signals, gates)

    print('Plotting fully fixed graph:')
    plot_graph()

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
