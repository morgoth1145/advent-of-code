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

MAP = {'one': 1,
       'two': 2,
       'three': 3,
       'four': 4,
       'five': 5,
       'six': 6,
       'seven': 7,
       'eight': 8,
       'nine': 9,
       'zero': 0}
for d in '0123456789':
    MAP[d] = int(d)

def part2(s):
    answer = 0

    for line in s.splitlines():
        best = None
        best_idx = None
        for a, d in MAP.items():
            if a in line:
                idx = line.index(a)
                if best_idx is None or best_idx > idx:
                    best = d
                    best_idx = idx

        val = best * 10

        line = line[::-1]

        best = None
        best_idx = None
        for a, d in MAP.items():
            a = a[::-1]
            if a in line:
                idx = line.index(a)
                if best_idx is None or best_idx > idx:
                    best = d
                    best_idx = idx

        val += best

        answer += val

    lib.aoc.give_answer(2023, 1, 2, answer)

INPUT = lib.aoc.get_input(2023, 1)
part1(INPUT)
part2(INPUT)
