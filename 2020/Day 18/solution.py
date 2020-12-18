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

def eval_helper(expression, part_merger):
    parts = list(tokenize(expression))
    for idx in range(0, len(parts), 2):
        p = parts[idx]
        if p[0] == '(':
            parts[idx] = eval_helper(p[1:-1], part_merger)
    return part_merger(parts)

def special_eval(expression):
    def part_merger(parts):
        while len(parts) > 1:
            a, op, b = parts[:3]
            parts = [eval(f'{a} {op} {b}')] + parts[3:]
        return int(parts[0])
    return eval_helper(expression, part_merger)

def part1(s):
    answer = sum(map(special_eval, s.splitlines()))
    print(f'The answer to part one is {answer}')

def advanced_special_eval(expression):
    def part_merger(parts):
        for op in '+*':
            while op in parts:
                idx = parts.index(op)
                val = eval(f'{parts[idx-1]} {op} {parts[idx+1]}')
                parts = parts[:idx-1] + [val] + parts[idx+2:]
        assert(len(parts) == 1)
        return int(parts[0])
    return eval_helper(expression, part_merger)

def part2(s):
    answer = sum(map(advanced_special_eval, s.splitlines()))
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 18)

part1(INPUT)
part2(INPUT)
