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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 16)
part1(INPUT)
part2(INPUT)
