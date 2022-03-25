import itertools

import lib.aoc

def phase(nums):
    out_nums = []

    for idx, n in enumerate(nums):
        repeat = idx+1
        val = 0

        offset = idx
        while offset < len(nums):
            val += sum(nums[offset:offset+repeat])
            offset += 2*repeat
            val -= sum(nums[offset:offset+repeat])
            offset += 2*repeat

        out_nums.append(abs(val) % 10)

    return out_nums

def part1(s):
    nums = list(map(int, s))

    for _ in range(100):
        nums = phase(nums)

    answer = ''.join(map(str, nums[:8]))

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(int, s))
    offset = int(s[:7])

    tot_length = len(nums) * 10000
    # Assuming the offset is far enough in then we can discard the *vast*
    # majority of the repeat list and compute each phase via partial sums,
    # summing from the right
    assert(offset * 2 - 1 >= tot_length)

    remain_length = tot_length - offset
    repeat_times = (remain_length + len(nums) - 1) // len(nums)
    reverse_nums = (nums[::-1] * repeat_times)[:remain_length]

    for _ in range(100):
        reverse_nums = [n%10 for n in itertools.accumulate(reverse_nums)]

    answer = ''.join(map(str, reverse_nums[-8:]))[::-1]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 16)
part1(INPUT)
part2(INPUT)
