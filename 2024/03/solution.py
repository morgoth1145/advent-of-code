import re

import lib.aoc

def part1(s):
    answer = 0

    for part in re.findall('mul\((\d{1,3}),(\d{1,3})\)', s):
        answer += int(part[0]) * int(part[1])

    lib.aoc.give_answer(2024, 3, 1, answer)

def part2(s):
    answer = 0

    include = True

    for part in re.findall('mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)',
                           s):
        if part == 'do()':
            include = True
        elif part == 'don\'t()':
            include = False
        elif include:
            a, b = tuple(map(int, part[4:-1].split(',')))
            answer += a * b

    lib.aoc.give_answer(2024, 3, 2, answer)

INPUT = lib.aoc.get_input(2024, 3)
part1(INPUT)
part2(INPUT)
