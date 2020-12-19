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

def part2(s):
    rule_list, messages = s.split('\n\n')
    rules = parse_rules(rule_list)

    regex_42 = gen_rule_regex(rules, 42)
    regex_31 = gen_rule_regex(rules, 31)

    # Delete these just to make sure they don't get hit elsewhere
    del rules[42]
    del rules[31]

    # Rule 8 is 42 | 42 8
    # That essentially means "repeat rule 42 one or more times"
    rules[8] = [f'(?:{regex_42})+']

    # Rule 11 is 42 31 | 42 11 31
    # That essentially means "Repeat rule 42 one or more times, then
    # repeat rule 31 the same number of times"
    min_rule_42_len = min(map(len, re.findall(regex_42, messages)))
    min_rule_31_len = min(map(len, re.findall(regex_31, messages)))
    min_rule_11_rep_len = min_rule_42_len+min_rule_31_len

    messages = messages.splitlines()
    max_msg_len = max(map(len, messages))

    max_reps = (max_msg_len + min_rule_11_rep_len - 1) // min_rule_11_rep_len

    rule_11 = [regex_42*times + regex_31*times
               for times in range(1, max_reps+1)]
    rules[11] = [f'(?:{"|".join(rule_11)})']

    validator = re.compile(gen_rule_regex(rules, 0))

    answer = len(list(filter(validator.fullmatch, messages)))
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 19)

part1(INPUT)
part2(INPUT)
