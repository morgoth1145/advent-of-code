import collections

import helpers.input

def part1(s):
    nums = list(map(int, s.split()))
    nums += [max(nums) + 3, 0]
    nums = sorted(nums)
    last = nums[0]
    diff_counts = collections.defaultdict(int)
    one_diffs = 0
    three_diffs = 0
    for n in nums[1:]:
        diff_counts[n-last] += 1
        last = n
    assert(max(diff_counts.keys()) <= 3)
    answer = diff_counts[1] * diff_counts[3]
    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(int, s.split()))
    nums += [max(nums) + 3, 0]
    nums = sorted(nums)
    arrangements = [1]
    for idx in range(1, len(nums)):
        count = sum(arrangements[i]
                    for i in range(idx)
                    if nums[idx] - nums[i] in (1, 2, 3))
        arrangements.append(count)
    answer = arrangements[-1]
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 10)

part1(INPUT)
part2(INPUT)
