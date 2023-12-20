import collections

import lib.aoc

def parse_input(s):
    m = {}

    for line in s.splitlines():
        a, b = line.split(' -> ')
        b = b.split(', ')

        if a == 'broadcaster':
            t = None
        else:
            t = a[0]
            a = a[1:]

        assert(a not in m)
        m[a] = (t, b)

    return m

def part1(s):
    data = parse_input(s)

    num_low = 0
    num_high = 0
    memory = {}

    input_map = collections.defaultdict(list)

    for node, (_, dests) in data.items():
        for d in dests:
            input_map[d].append(node)

    for node, (t, _) in data.items():
        if t is None:
            continue
        if t == '%':
            memory[node] = False
        if t == '&':
            memory[node] = {d:False
                            for d in input_map[node]}

    for _ in range(1000):
        todo = [(None, 'broadcaster', False)]

        while todo:
            new_todo = []

            for src, node, is_high_pulse in todo:
                if is_high_pulse:
                    num_high += 1
                else:
                    num_low += 1

                info = data.get(node)
                if info is None:
                    continue

                t, dests = info
                if t == '%':
                    if is_high_pulse:
                        continue
                    state = memory[node]
                    memory[node] = not state
                    for d in dests:
                        new_todo.append((node, d, not state))
                    continue
                if t == '&':
                    state = memory[node]
                    state[src] = is_high_pulse

                    if sum(state.values()) == len(state):
                        # All are high, send a low pulse
                        to_send = False
                    else:
                        to_send = True

                    for d in dests:
                        new_todo.append((node, d, to_send))
                    continue
                if t is None:
                    for d in dests:
                        new_todo.append((node, d, is_high_pulse))
                    continue
                assert(False)

            todo = new_todo

    answer = num_low * num_high

    print(num_low, num_high)

    lib.aoc.give_answer(2023, 20, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 20)
part1(INPUT)
part2(INPUT)
