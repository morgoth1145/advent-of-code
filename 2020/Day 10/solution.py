import functools

import helpers.input

def part1(s):
    nums = list(map(int, s.split()))
    nums += [max(nums) + 3, 0]
    nums = sorted(nums)
    last = nums[0]
    one_diffs = 0
    three_diffs = 0
    for n in nums[1:]:
        diff = abs(n-last)
        assert(diff in (1, 2, 3))
        if diff == 1:
            one_diffs += 1
        if diff == 3:
            three_diffs += 1
        last = n
    answer = one_diffs * three_diffs
    print(f'The answer to part one is {answer}')

@functools.lru_cache()
def count_arrangements(nums):
    if len(nums) in (0, 1):
        return 1
    count = 0
    n = nums[0]
    for idx in range(1, len(nums)):
        if abs(nums[idx] - n) in (1, 2, 3):
            count += count_arrangements(nums[idx:])
    return count

def part2(s):
    nums = list(map(int, s.split()))
    nums += [max(nums) + 3, 0]
    nums = sorted(nums)
    nums = tuple(nums)
    answer = count_arrangements(nums)
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 10)

part1(INPUT)
part2(INPUT)
