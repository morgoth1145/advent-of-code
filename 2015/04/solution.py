import hashlib

import lib.aoc

def part1(s):
    answer = 0
    while hashlib.md5((s + str(answer)).encode()).hexdigest()[:5] != '0' * 5:
        answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = 0
    while hashlib.md5((s + str(answer)).encode()).hexdigest()[:6] != '0' * 6:
        answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 4)
part1(INPUT)
part2(INPUT)
