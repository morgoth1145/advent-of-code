import hashlib

import lib.aoc

def part1(s):
    answer = 0
    while hashlib.md5((s + str(answer)).encode()).hexdigest()[:5] != '0' * 5:
        answer += 1

    lib.aoc.give_answer(2015, 4, 1, answer)

def part2(s):
    answer = 0
    while hashlib.md5((s + str(answer)).encode()).hexdigest()[:6] != '0' * 6:
        answer += 1

    lib.aoc.give_answer(2015, 4, 2, answer)

INPUT = lib.aoc.get_input(2015, 4)
part1(INPUT)
part2(INPUT)
