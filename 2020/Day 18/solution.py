import helpers.input

def tokenize(expression):
    paren_count = 0
    current = ''
    for idx, part in enumerate(expression.split()):
        if part[0] == '(':
            paren_count += part.count('(')
            current += f' {part}'
            continue
        if part[-1] == ')':
            current += f' {part}'
            paren_count -= part.count(')')
            if paren_count == 0:
                yield current.strip()
                current = ''
            continue
        if paren_count > 0:
            current += f' {part}'
            continue
        yield part
    assert(paren_count == 0)

def special_eval(expression):
    parts = list(tokenize(expression))
    while len(parts) > 1:
        a, op, b = parts[:3]
        if a[0] == '(':
            a = special_eval(a[1:-1])
        if b[0] == '(':
            b = special_eval(b[1:-1])
        if op == '+':
            val = int(a) + int(b)
        elif op == '*':
            val = int(a) * int(b)
        else:
            assert(False)
        parts = [str(val)] + parts[3:]
    return int(parts[0])

def part1(s):
    answer = sum(map(special_eval, s.splitlines()))
    print(f'The answer to part one is {answer}')

def advanced_special_eval(expression):
    parts = list(tokenize(expression))
    for idx in range(0, len(parts), 2):
        p = parts[idx]
        if p[0] == '(':
            parts[idx] = advanced_special_eval(p[1:-1])
    while '+' in parts:
        idx = parts.index('+')
        a = parts[idx-1]
        b = parts[idx+1]
        val = int(a) + int(b)
        parts = parts[:idx-1] + [val] + parts[idx+2:]
    while '*' in parts:
        idx = parts.index('*')
        a = parts[idx-1]
        b = parts[idx+1]
        val = int(a) * int(b)
        parts = parts[:idx-1] + [val] + parts[idx+2:]
    assert(len(parts) == 1)
    return int(parts[0])

def part2(s):
    answer = sum(map(advanced_special_eval, s.splitlines()))
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 18)

part1(INPUT)
part2(INPUT)
