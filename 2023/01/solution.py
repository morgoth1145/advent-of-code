import parse

import lib.aoc

def parse_all_ints(s):
    return list(map(lambda r:r[0], parse.findall('{:d}', s)))

def parse_input(s):
    for line in s.splitlines():
        nums = parse_all_ints(line)
        a = nums[0]
        b = nums[-1]
        while a > 10:
            a //= 10
        if b > 10:
            b = b % 10
        yield a * 10 + b

def part1(s):
    answer = sum(parse_input(s))

    lib.aoc.give_answer(2023, 1, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 1)
part1(INPUT)
part2(INPUT)
