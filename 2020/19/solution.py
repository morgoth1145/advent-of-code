import lib.aoc
import lib.cyk

def solve(s):
    rule_list, messages = s.split('\n\n')

    rules = []
    for line in rule_list.splitlines():
        num, options = line.split(': ')

        if options[0] == '"':
            # Single character
            assert(options[-1] == '"' and len(options) == 3)
            rules.append((lib.cyk.Symbol(num), options[1]))
            continue

        for opt in options.split(' | '):
            rules.append((lib.cyk.Symbol(num),
                          [lib.cyk.Symbol(part) for part in opt.split()]))

    cnf = lib.cyk.CNFGrammar(rules, lib.cyk.Symbol('0'))

    return len(list(filter(cnf.matches, messages.splitlines())))

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2020, 19, 1, answer)

def part2(s):
    # Replace rules 8 and 11
    s = s.replace('\n8: 42\n',
                  '\n8: 42 | 42 8\n')
    s = s.replace('\n11: 42 31\n',
                  '\n11: 42 31 | 42 11 31\n')

    answer = solve(s)

    lib.aoc.give_answer(2020, 19, 2, answer)

INPUT = lib.aoc.get_input(2020, 19)

part1(INPUT)
part2(INPUT)
