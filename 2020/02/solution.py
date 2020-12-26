import re

import lib.aoc

def count_valid_password(s, validator):
    valid_count = 0
    for m in re.finditer('(\d+)\-(\d+) (\w): (\w+)', s):
        n1, n2, c, password = m.groups()
        if validator(int(n1), int(n2), c, password.strip()):
            valid_count += 1
    return valid_count

def part1(s):
    def validator(mint, maxt, c, password):
        return mint <= password.count(c) <= maxt
    answer = count_valid_password(s, validator)
    print(f'The answer to part one is {answer}')

def part2(s):
    def validator(a, b, c, password):
        return (password[a-1] == c) ^ (password[b-1] == c)
    answer = count_valid_password(s, validator)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2020, 2)
part1(INPUT)
part2(INPUT)
