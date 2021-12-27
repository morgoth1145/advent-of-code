import collections

import lib.aoc

def is_nice(s):
    for bad in ('ab', 'cd', 'pq', 'xy'):
        if bad in s:
            return False
    repeat = False
    for l in 'abcdefghijklmnopqrstuvwxyz':
        if 2*l in s:
            repeat = True
            break
    if not repeat:
        return False
    vowels = collections.Counter(s)
    if vowels['a'] + vowels['e'] + vowels['i'] + vowels['o'] + vowels['u'] >= 3:
        return True
    return False

def part1(s):
    answer = sum(1 for line in s.splitlines()
                 if is_nice(line))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 5)
part1(INPUT)
part2(INPUT)
