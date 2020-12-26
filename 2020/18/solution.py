import helpers.input
import helpers.parsing

def special_eval(expression):
    def merger(parts):
        while len(parts) > 1:
            a, op, b = parts[:3]
            parts[:3] = [eval(f'{a} {op} {b}')]
        return parts[0]
    return helpers.parsing.eval_parenthesized_expression(expression, merger)

def part1(s):
    answer = sum(map(special_eval, s.splitlines()))
    print(f'The answer to part one is {answer}')

def advanced_special_eval(expression):
    def merger(parts):
        for op in '+*':
            while op in parts:
                idx = parts.index(op)
                a, op, b = parts[idx-1:idx+2]
                parts[idx-1:idx+2] = [eval(f'{a} {op} {b}')]
        return parts[0]
    return helpers.parsing.eval_parenthesized_expression(expression, merger)

def part2(s):
    answer = sum(map(advanced_special_eval, s.splitlines()))
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 18)

part1(INPUT)
part2(INPUT)
