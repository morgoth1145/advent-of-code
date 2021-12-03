from collections import Counter

import lib.aoc

def parse(s):
    nums = [int(n, 2)
            for n in s.split()]
    bits = len(s.split()[0])
    masks = [2**b
             for b in range(bits-1, -1, -1)]
    return nums, masks

def most_least(nums, mask):
    return Counter(n & mask for n in nums).most_common(2)

def part1(s):
    nums, masks = parse(s)

    gamma, epsilon = 0, 0

    for m in masks:
        most, least = most_least(nums, m)
        gamma |= most[0]
        epsilon |= least[0]

    answer = gamma * epsilon

    print(f'The answer to part one is {answer}')

def part2(s):
    nums, masks = parse(s)

    oxy_cands, co2_cands = nums, nums

    for m in masks:
        if len(oxy_cands) > 1:
            most, least = most_least(oxy_cands, m)
            target = most[0]
            if most[1] == least[1]:
                target = m
            oxy_cands = [n for n in oxy_cands if n & m == target]
        if len(co2_cands) > 1:
            most, least = most_least(co2_cands, m)
            target = least[0]
            if most[1] == least[1]:
                target = 0
            co2_cands = [n for n in co2_cands if n & m == target]

    answer = oxy_cands[0]*co2_cands[0]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 3)
part1(INPUT)
part2(INPUT)
