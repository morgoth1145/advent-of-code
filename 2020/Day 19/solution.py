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

def prune_unreachable(rules):
    while True:
        referenced = {0}
        for options in rules.values():
            for o in options:
                if isinstance(o, str):
                    continue
                for item in o:
                    referenced.add(item)
        progress = False
        new_rules = {}
        for num, options in rules.items():
            if num not in referenced:
                progress = True
                continue
            new_rules[num] = options
        if not progress:
            return rules
        rules = new_rules

def part1(s):
    rule_list, messages = s.split('\n\n')
    letters_to_nums, rules = parse_rules(rule_list)

    options_for_42 = set(iter_possibilities(rules, 42))
    options_for_31 = set(iter_possibilities(rules, 31))
    rules[42] = options_for_42
    rules[31] = options_for_31
    rules = prune_unreachable(rules)

    possibilities = set(iter_possibilities(rules, 0))
    answer = 0
    for msg in messages.splitlines():
        if msg in possibilities:
            answer += 1
    print(f'The answer to part one is {answer}')

def iter_bounded_possibilities(rules, start, max_length, memo={}):
    key = (start, max_length)
    answer = memo.get(key)
    if answer is not None:
        yield from answer
        return
    answer = []
    if max_length <= 0:
        return
    for o in rules[start]:
        if isinstance(o, str):
            if len(o) <= max_length:
                answer.append(o)
                yield o
            continue
        candidate_options = []
        sub_max_length = max_length
        for idx, item in enumerate(o):
            if isinstance(item, str):
                candidate_options.append([item])
                sub_max_length -= len(item)
            else:
                sub_options = list(iter_bounded_possibilities(rules,
                                                              item,
                                                              sub_max_length,
                                                              memo))
                sub_options = set(sub_options)
                if '' in sub_options:
                    sub_options.remove('')
                if len(sub_options) > 0:
                    sub_max_length -= min(map(len, sub_options))
                    candidate_options.append(sub_options)
        expanded = list(expand_thingy(candidate_options))
        yield from expanded
        answer.extend(expanded)
    answer = set(answer)
    memo[key] = answer

def preprocess_message(msg, options_for_42, options_for_31):
    length = set(map(len, options_for_42)) | set(map(len, options_for_31))
    assert(len(length) == 1)
    length = list(length)[0]
    if len(msg) % length != 0:
        return None
    answer = ''
    for idx in range(0, len(msg), length):
        if msg[idx:idx+length] in options_for_42:
            answer += 'c'
        elif msg[idx:idx+length] in options_for_31:
            answer += 'd'
        else:
            return None
    return answer

def part2(s):
    rule_list, messages = s.split('\n\n')
    letters_to_nums, rules = parse_rules(rule_list)
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    options_for_42 = set(iter_possibilities(rules, 42))
    options_for_31 = set(iter_possibilities(rules, 31))
    rules[42] = 'c'
    rules[31] = 'd'

    rules = prune_unreachable(rules)

    messages = messages.split()
    messages = [preprocess_message(msg, options_for_42, options_for_31)
                for msg in messages]
    messages = [msg for msg in messages if msg is not None]

    max_length = max(map(len, messages))

    possibilities = set(iter_bounded_possibilities(rules, 0, max_length))

    answer = 0
    for msg in messages:
        if msg in possibilities:
            answer += 1
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 19)

part1(INPUT)
part2(INPUT)
