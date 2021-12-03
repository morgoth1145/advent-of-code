import lib.aoc

def parse(s):
    nums = [int(n, 2)
            for n in s.split()]
    bits = len(s.split()[0])
    masks = [2**b
             for b in range(bits-1, -1, -1)]
    return nums, masks

def split_list(nums, mask):
    ones = []
    zeros = []
    for n in nums:
        if n & mask:
            ones.append(n)
        else:
            zeros.append(n)
    return ones, zeros

def part1(s):
    nums, masks = parse(s)

    gamma, epsilon = 0, 0

    for m in masks:
        ones, zeros = split_list(nums, m)

        if len(ones) > len(zeros):
            gamma |= m
        else:
            epsilon |= m

    answer = gamma * epsilon

    print(f'The answer to part one is {answer}')

def part2(s):
    nums, masks = parse(s)

    oxy_cands, co2_cands = nums, nums

    for m in masks:
        if len(oxy_cands) > 1:
            ones, zeros = split_list(oxy_cands, m)
            oxy_cands = ones if len(ones) >= len(zeros) else zeros
        if len(co2_cands) > 1:
            ones, zeros = split_list(co2_cands, m)
            co2_cands = ones if len(ones) < len(zeros) else zeros

    answer = oxy_cands[0]*co2_cands[0]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 3)
part1(INPUT)
part2(INPUT)
