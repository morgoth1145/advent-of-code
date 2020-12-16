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

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 16)

part1(INPUT)
part2(INPUT)
