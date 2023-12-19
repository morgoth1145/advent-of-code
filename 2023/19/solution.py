import lib.aoc

def make_test(var, op, val):
    if op == '<':
        return lambda part: part[var] < val
    elif op == '>':
        return lambda part: part[var] > val
    else:
        assert(False)

def make_test_2(op, val):
    if op == '<':
        return lambda n: n < val
    elif op == '>':
        return lambda n: n > val
    else:
        assert(False)

def parse_input(s):
    a, b = s.split('\n\n')

    workflows = {}
    parts = []

    a = a.replace('{', ' ').replace('}', '')

    for line in a.splitlines():
        name, rules = line.split()

        rule_list = []

        for r in rules.split(','):
            if ':' in r:
                pred, dest = r.split(':')
                var = pred[0]
                op = pred[1]
                val = int(pred[2:])
                rule_list.append((make_test(var, op, val), dest, var, val,
                                  make_test_2(op, val)))
            else:
                rule_list.append(r)

        workflows[name] = rule_list

    for c in 'xmas':
        b = b.replace(f'{c}=', f'"{c}":')

    for line in b.splitlines():
        parts.append(eval(line))

    return workflows, parts

def part1(s):
    workflows, parts = parse_input(s)

    answer = 0

    for idx, p in enumerate(parts):
        name = 'in'
        while True:
            rules = workflows[name]
            dest = None
            for r in rules:
                if isinstance(r, tuple):
                    if r[0](p):
                        dest = r[1]
                        break
                else:
                    dest = r
                    break

            assert(dest is not None)

            if dest == 'A':
                answer += sum(p.values())
                break

            elif dest == 'R':
                break

            name = dest

    lib.aoc.give_answer(2023, 19, 1, answer)

def part2(s):
    workflows, _ = parse_input(s)

    def count_accepted(w_name, x, m, a, s):
        if w_name == 'A':
            return len(x) * len(m) * len(a) * len(s)
        if w_name == 'R':
            return 0

        rules = workflows[w_name]

        c = 0

        for r in rules:
            if isinstance(r, tuple):
                dest = r[1]
                var = r[2]
                test2 = r[4]

                if var == 'x':
                    take_x = tuple(filter(test2, x))
                    if len(take_x):
                        c += count_accepted(dest, take_x, m, a, s)
                    x = tuple(n for n in x if not test2(n))
                elif var == 'm':
                    take_m = tuple(filter(test2, m))
                    if len(take_m):
                        c += count_accepted(dest, x, take_m, a, s)
                    m = tuple(n for n in m if not test2(n))
                elif var == 'a':
                    take_a = tuple(filter(test2, a))
                    if len(take_a):
                        c += count_accepted(dest, x, m, take_a, s)
                    a = tuple(n for n in a if not test2(n))
                elif var == 's':
                    take_s = tuple(filter(test2, s))
                    if len(take_s):
                        c += count_accepted(dest, x, m, a, take_s)
                    s = tuple(n for n in s if not test2(n))
            else:
                c += count_accepted(r, x, m, a, s)

        return c

    answer = count_accepted('in',
                            tuple(range(1, 4001)),
                            tuple(range(1, 4001)),
                            tuple(range(1, 4001)),
                            tuple(range(1, 4001)))

    lib.aoc.give_answer(2023, 19, 2, answer)

INPUT = lib.aoc.get_input(2023, 19)
part1(INPUT)
part2(INPUT)
