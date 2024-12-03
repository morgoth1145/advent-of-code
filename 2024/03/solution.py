import re

import lib.aoc

def part1(s):
    answer = 0

    for group in re.findall('mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)', s):
        answer += int(group[0]) * int(group[1])

    lib.aoc.give_answer(2024, 3, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 3)
part1(INPUT)
part2(INPUT)
