import json

import lib.aoc

def parse_input(s):
    # Remove ignores
    garbage_s = ''
    while s:
        idx = s.find('!')
        if idx == -1:
            garbage_s += s
            s = ''
        else:
            garbage_s += s[:idx]
            s = s[idx+2:]

    discarded = 0

    clean_s = ''
    # Remove garbage
    while garbage_s:
        idx = garbage_s.find('<')
        if idx == -1:
            clean_s += garbage_s
            garbage_s = ''
        else:
            clean_s += garbage_s[:idx]
            end_idx = garbage_s.find('>', idx)
            discarded += end_idx - idx - 1
            garbage_s = garbage_s[end_idx+1:]

    assert(len(set(clean_s) - set('{},')) == 0)

    s = clean_s.translate(str.maketrans('{}', '[]'))
    while ',,' in s:
        s = s.replace(',,', ',')
    s = s.replace('[,', '[')
    s = s.replace(',]', ']')
    return json.loads(s), discarded

def score(tree, parent_score=0):
    self = parent_score + 1
    return self + sum(score(child, self)
                      for child in tree)

def part1(s):
    answer = score(parse_input(s)[0])

    print(f'The answer to part one is {answer}')

def part2(s):
    _, answer = parse_input(s)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 9)
part1(INPUT)
part2(INPUT)
