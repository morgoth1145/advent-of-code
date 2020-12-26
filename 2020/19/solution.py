import functools
import re

import lib.aoc

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

    assert(rules[0] == [(8, 11)])
    # Given that rule 0 is 8 11
    # And rule 8 is 42 | 42 8 (from the problem description)
    # And rule 11 is 42 31 | 42 11 31 (from the problem description)
    # We can make a simple regex and do post-validation.
    # Rule 8 is <rule_42>+
    # Rule 11 is <rule_42>{n}<rule_31>{n} (for any n)
    # So rule 0 is <rule_42>{n}<rule_31>{m} (for n > m)
    # We can write this as ((?:<rule_42>)+)((?:<rule_11>)+), so long as
    # we then verify that capture group 1 is repeated more than capture group 2!
    # It turns out that rule_42 and rule_11 match strings of the same length, so
    # we just need to check the length of each group.
    regex_0 = re.compile(f'((?:{regex_42})+)((?:{regex_31})+)')

    def validator(msg):
        m = regex_0.fullmatch(msg)
        return m is not None and len(m.group(1)) > len(m.group(2))

    answer = len(list(filter(validator, messages.split())))
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2020, 19)

part1(INPUT)
part2(INPUT)
