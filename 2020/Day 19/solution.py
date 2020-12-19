import helpers.input

def parse_rules(rule_list):
    letters_to_nums = {}
    rules = {}
    for line in rule_list.splitlines():
        num, rule = line.split(': ')
        num = int(num)
        if rule[0] == '"':
            rule = rule[1] # Single character
            rules[num] = [rule]
            letters_to_nums[rule] = num
            continue
        options = []
        for opt in rule.split('|'):
            options.append(tuple(map(int, opt.split())))
        rules[num] = options
    return letters_to_nums, rules

def expand_thingy(candidate_options):
    if len(candidate_options) == 0:
        yield ''
        return
    for o in candidate_options[0]:
        for sub_bit in expand_thingy(candidate_options[1:]):
            yield o + sub_bit

def iter_possibilities(rules, start, memo={}):
    answers = memo.get(start)
    if answers is not None:
        yield from answers
        return
    answers = []
    for o in rules[start]:
        if isinstance(o, str):
            answers.append(o)
            yield o
            continue
        candidate_options = []
        for item in o:
            if isinstance(item, str):
                candidate_options.append([item])
            else:
                candidate_options.append(list(iter_possibilities(rules,
                                                                 item,
                                                                 memo)))
        expanded = list(expand_thingy(candidate_options))
        yield from expanded
        answers.extend(expanded)
    memo[start] = answers

def part1(s):
    rule_list, messages = s.split('\n\n')
    letters_to_nums, rules = parse_rules(rule_list)
    possibilities = set(iter_possibilities(rules, 0))
    answer = 0
    for msg in messages.splitlines():
        if msg in possibilities:
            answer += 1
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 19)

part1(INPUT)
part2(INPUT)
