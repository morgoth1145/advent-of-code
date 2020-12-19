import helpers.input
import helpers.parsing

def special_eval(expression):
    def merger(tree):
        while len(tree) > 1:
            a, op, b = tree[:3]
            if isinstance(a, list): a = merger(a)
            if isinstance(b, list): b = merger(b)
            tree[:3] = [eval(f'{a} {op} {b}')]
        return tree[0]
    tree = helpers.parsing.get_parenthesized_expression_parse_tree(expression)
    return merger(tree)

def part1(s):
    answer = sum(map(special_eval, s.splitlines()))
    print(f'The answer to part one is {answer}')

def advanced_special_eval(expression):
    def merger(tree):
        for op in '+*':
            while op in tree:
                idx = tree.index(op)
                a, op, b = tree[idx-1:idx+2]
                if isinstance(a, list): a = merger(a)
                if isinstance(b, list): b = merger(b)
                tree[idx-1:idx+2] = [eval(f'{a} {op} {b}')]
        return tree[0]
    tree = helpers.parsing.get_parenthesized_expression_parse_tree(expression)
    return merger(tree)

def part2(s):
    answer = sum(map(advanced_special_eval, s.splitlines()))
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 18)

part1(INPUT)
part2(INPUT)
