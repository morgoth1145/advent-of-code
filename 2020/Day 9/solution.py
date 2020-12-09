import itertools

import helpers.input

def get_invalid_num(nums):
    for idx, n in enumerate(nums[25:]):
        options = set(nums[idx:idx+25])
        if not any(n-v in options
                   for v
                   in options):
            return n

def part1(s):
    nums = list(map(int, s.split()))
    answer = get_invalid_num(nums)
    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(int, s.split()))
    target = get_invalid_num(nums)
    sums = list(itertools.accumulate(nums))
    for idx, a in enumerate(sums):
        for idx2, b in enumerate(sums[idx+1:]):
            diff = b - a
            if diff > target:
                break
            if diff == target:
                the_nums = nums[idx+1:idx+idx2+2]
                assert(sum(the_nums) == target)
                answer = min(the_nums) + max(the_nums)
                print(f'The answer to part two is {answer}')
                return

INPUT = helpers.input.get_input(2020, 9)

part1(INPUT)
part2(INPUT)