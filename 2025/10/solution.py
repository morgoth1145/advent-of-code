import z3

import lib.aoc
import lib.graph

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
        matched = False
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
                    if ns == target:
                        matched = True
                        break
                    new_states.add(ns)
                if matched:
                    break

            if matched:
                break

            todo = new_states - handled
            handled.update(new_states)

        assert(matched)
        answer += steps

    lib.aoc.give_answer(2025, 10, 1, answer)

def part2_graph_search_nonsense(s):
    import time

    data = list(parse_input(s))

    answer = 0

    start_t = time.perf_counter()

    for i, (_, buttons, joltage) in enumerate(data):
        now = time.perf_counter()
        min_button_len = min(map(len, buttons))

        print(now-start_t,
              i, len(data), sum(joltage), len(buttons), min_button_len)

        start = (0,) * len(joltage)

        def neighbor_fn(state):
            if state == joltage:
                return

            bad_jolt_indices = list(i
                                    for i, (a, b)
                                    in enumerate(zip(state, joltage))
                                    if a < b)

            best_num_buttons = len(buttons)*2
            worst_idx = None
            for idx in bad_jolt_indices:
                num_buttons = sum(1 for b in buttons
                                  if idx in b
                                  if all(joltage[p] >= state[p]
                                         for p in b))

                if num_buttons < best_num_buttons:
                    best_num_buttons = num_buttons
                    worst_idx = idx

            bad_jolt_idx = worst_idx

            valid_buttons = [b for b in buttons
                             if bad_jolt_idx in b
                             if all(joltage[p] >= state[p]
                                    for p in b)]

            steps_to_take = joltage[bad_jolt_idx] - state[bad_jolt_idx]

            def gen_states(state, rem_buttons, rem_steps):
                if rem_steps == 0:
                    yield state
                    return

                if len(rem_buttons) == 0:
                    return

                ns = list(state)

                b = rem_buttons[0]
                for i in range(rem_steps+1):
                    yield from gen_states(tuple(ns),
                                          rem_buttons[1:],
                                          rem_steps-i)
                    for p in b:
                        ns[p] += 1

                    if any(a > b for a,b in zip(ns, joltage)):
                        return

            for s in gen_states(state, valid_buttons, steps_to_take):
                yield s, steps_to_take

        graph = lib.graph.make_lazy_graph(neighbor_fn)

        def heuristic(state):
            rem_joltage = sum(b-a for a, b in zip(state, joltage))
            return (rem_joltage + min_button_len - 1) // min_button_len

        steps = lib.graph.find_shortest_path_length(graph,
                                                    start,
                                                    joltage,
                                                    heuristic
                                                    )

        assert(steps >= 0)

        answer += steps

    lib.aoc.give_answer(2025, 10, 2, answer)

def part2(s):
    data = list(parse_input(s))

    answer = 0

    for i, (_, buttons, joltage) in enumerate(data):
        o = z3.Optimize()

        button_vars = []

        for b in range(len(buttons)):
            bv = z3.Int('button' + str(b))
            button_vars.append(bv)
            o.add(bv >= 0)

        for jidx, j in enumerate(joltage):
            jv = z3.Int('jolt' + str(j))
            jeq = j

            for b, bv in zip(buttons, button_vars):
                if jidx in b:
                    jeq = jeq - bv

            o.add(jeq == 0)

        steps = z3.Int('steps')

        steps_eq = 0

        for bv in button_vars:
            steps_eq = steps_eq + bv

        o.add(steps == steps_eq)

        o.minimize(steps)
        o.check()
        steps_val = o.model()[steps].as_long()

        answer += steps_val

    lib.aoc.give_answer(2025, 10, 2, answer)

part2 = part2_graph_search_nonsense

INPUT = lib.aoc.get_input(2025, 10)
part1(INPUT)
part2(INPUT)
