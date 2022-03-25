import lib.aoc

def make_mask(idx, length):
    idx += 1
    mask = []

    while len(mask) < length+1:
        for n in (0, 1, 0, -1):
            mask += [n] * idx

    return mask[1:length+1]

def phase(nums):
    out_nums = []

    for idx, n in enumerate(nums):
        val = abs(sum(d*m for d, m in zip(nums, make_mask(idx, len(nums)))))
        out_nums.append(val % 10)

    return out_nums

def part1(s):
    nums = list(map(int, s))

    for _ in range(100):
        nums = phase(nums)

    answer = ''.join(map(str, nums[:8]))

    print(f'The answer to part one is {answer}')

def partial_sums_mod_10(nums):
    out_nums = []

    s = 0
    for n in nums:
        s += n
        out_nums.append(s % 10)

    return out_nums

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
        reverse_nums = partial_sums_mod_10(reverse_nums)

    answer = ''.join(map(str, reverse_nums[-8:]))[::-1]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 16)
part1(INPUT)
part2(INPUT)
