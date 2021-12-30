import itertools

import lib.aoc

def part1(s):
    nums = list(map(int, s.splitlines()))

    answer = 0

    for l in range(len(nums)):
        for combo in itertools.combinations(nums, l):
            if sum(combo) == 150:
                answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(int, s.splitlines()))

    answer = 0

    for l in range(len(nums)):
        for combo in itertools.combinations(nums, l):
            if sum(combo) == 150:
                answer += 1
        if answer > 0:
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 17)
part1(INPUT)
part2(INPUT)
