import re

import lib.aoc

def parse_input(s):
    raw_rules, my_ticket, nearby = s.split('\n\n')

    rules = {}
    for rule in raw_rules.splitlines():
        m = re.match('(.*): (\d+)\-(\d+) or (\d+)\-(\d+)', rule)
        name = m.group(1)
        range_1 = range(int(m.group(2)), int(m.group(3))+1)
        range_2 = range(int(m.group(4)), int(m.group(5))+1)
        rules[name] = set(range_1) | set(range_2)

    my_ticket = list(map(int, my_ticket.splitlines()[1].split(',')))

    nearby = [list(map(int, l.split(','))) for l in nearby.splitlines()[1:]]

    return rules, my_ticket, nearby

def part1(s):
    rules, _, nearby = parse_input(s)

    answer = 0
    for ticket in nearby:
        for n in ticket:
            if not any(n in nums for nums in rules.values()):
                answer += n

    lib.aoc.give_answer(2020, 16, 1, answer)

def part2(s):
    rules, my_ticket, nearby = parse_input(s)

    # Filter to the good nearby tickets
    nearby = [ticket for ticket in nearby
              if all(any(n in nums for nums in rules.values())
                     for n in ticket)]

    rule_order_candidates = []
    for vals in zip(*nearby):
        candidates = set()
        for name, valid_nums in rules.items():
            if all(v in valid_nums for v in vals):
                candidates.add(name)
        rule_order_candidates.append(candidates)

    rule_order = [None] * len(rule_order_candidates)
    for _ in range(len(rule_order)):
        for idx, candidates in enumerate(rule_order_candidates):
            if rule_order[idx] is None and 1 == len(candidates):
                (rule_order[idx],) = candidates
                for j, old_candidates in enumerate(rule_order_candidates):
                    rule_order_candidates[j] = old_candidates - candidates
                break
    assert(None not in rule_order)

    answer = 1
    for name, val in zip(rule_order, my_ticket):
        if name.startswith('departure'):
            answer *= val

    lib.aoc.give_answer(2020, 16, 2, answer)

INPUT = lib.aoc.get_input(2020, 16)

part1(INPUT)
part2(INPUT)
