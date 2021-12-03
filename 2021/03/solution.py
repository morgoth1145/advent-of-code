import lib.aoc

def determine_common(nums, bit, default=None):
    c1 = 0
    c0 = 0
    for n in nums:
        if n[bit] == '1':
            c1 += 1
        else:
            c0 += 1

    if c1 == c0 and default is not None:
        return default, default

    if c1 > c0:
        return '1', '0'
    else:
        return '0', '1'

def part1(s):
    nums = []
    for n in s.split():
        nums.append(n)

    bits = len(s.split()[0])

    gamma = []
    epsilon = []

    for b in range(bits):
        most, least = determine_common(nums, b)

        gamma.append(most)
        epsilon.append(least)

    gamma = int(''.join(gamma), base=2)
    epsilon = int(''.join(epsilon), base=2)

    answer = gamma*epsilon

    print(f'The answer to part one is {answer}')

def filter_matching(cands, bit, target):
    out = []
    for n in cands:
        if n[bit] == target:
            out.append(n)
    return out

def part2(s):
    nums = []
    for n in s.split():
        nums.append(n)

    oxy_cands = nums[:]
    co2_cands = nums[:]

    bits = len(s.split()[0])

    for b in range(bits):
        if len(oxy_cands) > 1:
            most, least = determine_common(oxy_cands, b, '1')
            oxy_cands = filter_matching(oxy_cands, b, most)
        if len(co2_cands) > 1:
            most, least = determine_common(co2_cands, b, '0')
            co2_cands = filter_matching(co2_cands, b, least)

    oxy = int(''.join(oxy_cands[0]), base=2)
    co2 = int(''.join(co2_cands[0]), base=2)

    answer = oxy*co2

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 3)
part1(INPUT)
part2(INPUT)
