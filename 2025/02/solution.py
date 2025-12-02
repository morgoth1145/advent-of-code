import re

import lib.aoc

def solve(s, pattern):
    r = re.compile(pattern)

    answer = 0

    for span in s.split(','):
        a, b = span.split('-')

        for n in range(int(a), int(b)+1):
            if r.fullmatch(str(n)):
                answer += n

    return answer

def part1(s):
    # Single repetition
    answer = solve(s, '(\\d+)\\1')

    lib.aoc.give_answer(2025, 2, 1, answer)

def part2(s):
    # 2+ repetitions 
    answer = solve(s, '(\\d+)\\1+')

    lib.aoc.give_answer(2025, 2, 2, answer)

INPUT = lib.aoc.get_input(2025, 2)
part1(INPUT)
part2(INPUT)
