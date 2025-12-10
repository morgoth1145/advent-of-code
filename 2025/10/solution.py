import z3

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        target = None
        buttons = []
        joltage = None

        parts = line.split()
        for p in parts:
            cs, ce = p[0], p[-1]
            if cs + ce == '[]':
                assert(target is None)
                target = p[1:-1]
            elif cs + ce == '()':
                buttons.append(tuple(sorted(map(int, p[1:-1].split(',')))))
            elif cs + ce == '{}':
                assert(joltage is None)
                joltage = tuple(map(int, p[1:-1].split(',')))
            else:
                assert(False)

        yield target, sorted(buttons), joltage

def part1(s):
    data = list(parse_input(s))

    answer = 0

    for target, buttons, _ in data:
        todo = ['.' * len(target)]
        handled = set(todo)
        steps = 0

        while True:
            steps += 1

            assert(len(todo) > 0)

            new_states = set()

            for state in todo:
                state = list(state)
                for b in buttons:
                    ns = state[:]
                    for p in b:
                        ns[p] = '.' if ns[p] == '#' else '#'
                    ns = ''.join(ns)
                    new_states.add(ns)

            if target in new_states:
                answer += steps
                break

            todo = new_states - handled
            handled.update(new_states)

    lib.aoc.give_answer(2025, 10, 1, answer)

def part2(s):
    data = list(parse_input(s))

    answer = 0

    for i, (_, buttons, joltage) in enumerate(data):
        o = z3.Optimize()

        button_vars = []

        for b in range(len(buttons)):
            bv = z3.Int(f'button{b}')
            button_vars.append(bv)
            o.add(bv >= 0)

        for jidx, j in enumerate(joltage):
            jv = z3.Int(f'jolt{j}')

            jeq = sum(bv
                      for b, bv
                      in zip(buttons, button_vars)
                      if jidx in b)

            o.add(jeq == j)

        steps = z3.Int('steps')
        o.add(steps == sum(button_vars))

        o.minimize(steps)
        o.check()

        answer += o.model()[steps].as_long()

    lib.aoc.give_answer(2025, 10, 2, answer)

INPUT = lib.aoc.get_input(2025, 10)
part1(INPUT)
part2(INPUT)
