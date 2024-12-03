import re

import lib.aoc

def part1(s):
    answer = 0

    for group in re.findall('mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)', s):
        answer += int(group[0]) * int(group[1])

    lib.aoc.give_answer(2024, 3, 1, answer)

def part2(s):
    answer = 0

    parts = s.split('don\'t()')
    parts[0] = 'do()' + parts[0]

    to_handle = ''

    for p in parts:
        if 'do()' in p:
            i = p.index('do()')
            to_handle += p[i:]

    for group in re.findall('mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)',
                            to_handle):
        answer += int(group[0]) * int(group[1])

    lib.aoc.give_answer(2024, 3, 2, answer)

INPUT = lib.aoc.get_input(2024, 3)
part1(INPUT)
part2(INPUT)
