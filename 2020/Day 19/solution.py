import functools
import re

import helpers.input

def parse_rules(rule_list):
    rules = {}
    for line in rule_list.splitlines():
        num, rule = line.split(': ')
        num = int(num)
        if rule[0] == '"':
            rule = rule[1] # Single character
            rules[num] = [rule]
            continue
        options = []
        for opt in rule.split('|'):
            options.append(tuple(map(int, opt.split())))
        rules[num] = options
    return rules

def gen_rule_regex(rules, start):
    @functools.lru_cache()
    def impl(start):
        parts = []
        for option in rules[start]:
            if isinstance(option, str):
                parts.append(option)
            else:
                parts.append(''.join(impl(item) for item in option))
        if len(parts) == 1:
            return parts[0]
        return '(?:' + '|'.join(parts) + ')'
    return impl(start)

def part1(s):
    rule_list, messages = s.split('\n\n')
    rules = parse_rules(rule_list)

    validator = re.compile(gen_rule_regex(rules, 0))

    answer = len(list(filter(validator.fullmatch, messages.splitlines())))
    print(f'The answer to part one is {answer}')

def expand_candidates(candidate_options):
    if len(candidate_options) == 0:
        yield ''
        return
    for o in candidate_options[0]:
        for sub_bit in expand_candidates(candidate_options[1:]):
            yield o + sub_bit

def gen_possibilities(rules, start):
    @functools.lru_cache()
    def impl(start):
        answers = []
        for o in rules[start]:
            if isinstance(o, str):
                answers.append(o)
                continue
            candidate_options = []
            for item in o:
                if isinstance(item, str):
                    candidate_options.append([item])
                else:
                    candidate_options.append(impl(item))
            answers.extend(expand_candidates(candidate_options))
        return answers
    return impl(start)

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

def gen_bounded_possibilities(rules, start, max_length):
    def impl(start, max_length):
        answer = []
        if max_length <= 0:
            return []
        for o in rules[start]:
            if isinstance(o, str):
                if len(o) <= max_length:
                    answer.append(o)
                continue
            candidate_options = []
            sub_max_length = max_length
            for idx, item in enumerate(o):
                if isinstance(item, str):
                    candidate_options.append([item])
                    sub_max_length -= len(item)
                else:
                    sub_options = impl(item, sub_max_length)
                    if len(sub_options) > 0:
                        sub_max_length -= min(map(len, sub_options))
                        candidate_options.append(sub_options)
            answer.extend(expand_candidates(candidate_options))
        return answer
    return impl(start, max_length)

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
    rules = parse_rules(rule_list)
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    options_for_42 = gen_possibilities(rules, 42)
    options_for_31 = gen_possibilities(rules, 31)
    rules[42] = 'c'
    rules[31] = 'd'

    rules = prune_unreachable(rules)

    messages = messages.split()
    messages = [preprocess_message(msg, options_for_42, options_for_31)
                for msg in messages]
    messages = [msg for msg in messages if msg is not None]

    max_length = max(map(len, messages))

    possibilities = set(gen_bounded_possibilities(rules, 0, max_length))

    answer = 0
    for msg in messages:
        if msg in possibilities:
            answer += 1
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 19)

part1(INPUT)
part2(INPUT)
