import re

import helpers.input

def part1(s):
    rules, my_ticket, nearby = s.split('\n\n')

    rules = rules.splitlines()

    _, my_ticket = my_ticket.splitlines()
    my_ticket = list(map(int, my_ticket.split(',')))

    nearby = [list(map(int, l.split(','))) for l in nearby.splitlines()[1:]]

    valid_numbers = set()
    for rule in rules:
        m = re.match('(.*): (\d+)\-(\d+) or (\d+)\-(\d+)', rule)
        name = m.group(1)
        range_1 = range(int(m.group(2)), int(m.group(3))+1)
        range_2 = range(int(m.group(4)), int(m.group(5))+1)
        valid_numbers |= set(range_1)
        valid_numbers |= set(range_2)

    answer = 0
    for ticket in nearby:
        for n in ticket:
            if n not in valid_numbers:
                answer += n

    print(f'The answer to part one is {answer}')

# TODO: This can probably be done better
def determine_rule_order(available, rule_order_candidates):
    if 0 == len(rule_order_candidates):
        return []

    candidates = rule_order_candidates[0]
    rest = rule_order_candidates[1:]

    for name in candidates:
        if name in available:
            answer = determine_rule_order(available - {name}, rest)
            if answer is not None:
                return [name] + answer

def part2(s):
    rules, my_ticket, nearby = s.split('\n\n')

    rules = rules.splitlines()

    _, my_ticket = my_ticket.splitlines()
    my_ticket = list(map(int, my_ticket.split(',')))

    nearby = [list(map(int, l.split(','))) for l in nearby.splitlines()[1:]]

    parsed_rules = {}
    valid_numbers = set()
    for rule in rules:
        m = re.match('(.*): (\d+)\-(\d+) or (\d+)\-(\d+)', rule)
        name = m.group(1)
        range_1 = range(int(m.group(2)), int(m.group(3))+1)
        range_2 = range(int(m.group(4)), int(m.group(5))+1)
        valid_numbers |= set(range_1)
        valid_numbers |= set(range_2)
        parsed_rules[name] = set(range_1) | set(range_2)

    good_nearby = []
    for ticket in nearby:
        is_valid = True
        for n in ticket:
            if n not in valid_numbers:
                is_valid = False
                break
        if is_valid:
            good_nearby.append(ticket)

    rule_order_candidates = []
    for vals in zip(*good_nearby):
        candidates = set()
        for name, valid_nums in parsed_rules.items():
            if all(v in valid_nums for v in vals):
                candidates.add(name)
        rule_order_candidates.append(candidates)

    rule_order = determine_rule_order(set(parsed_rules.keys()), rule_order_candidates)

    answer = 1
    for name, val in zip(rule_order, my_ticket):
        if name.startswith('departure'):
            answer *= val

    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 16)

part1(INPUT)
part2(INPUT)
