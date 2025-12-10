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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 10)
part1(INPUT)
part2(INPUT)
