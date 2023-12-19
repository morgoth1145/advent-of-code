import lib.aoc

def make_test(var, op, val):
    if op == '<':
        return lambda part: part[var] < val
    elif op == '>':
        return lambda part: part[var] > val
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
                rule_list.append((make_test(var, op, val), dest))
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
    pass

INPUT = lib.aoc.get_input(2023, 19)
part1(INPUT)
part2(INPUT)
