import lib.aoc

def knot_hash(nums, pos, skip, lengths):
    nums = list(nums)

    for l in lengths:
        # Reverse
        to_rev = []
        for i in range(l):
            to_rev.append(nums[(pos + i) % len(nums)])
        for i, v in enumerate(to_rev[::-1]):
            nums[(pos + i) % len(nums)] = v

        pos = (pos + l + skip) % len(nums)
        skip += 1

    return nums, pos, skip

def part1(s):
    nums = list(range(256))
    lengths = list(map(int, s.split(',')))

    nums, _, _ = knot_hash(nums, 0, 0, lengths)

    answer = nums[0] * nums[1]

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(range(256))
    lengths = list(map(ord, s)) + [17, 31, 73, 47, 23]

    pos, skip = 0, 0

    for _ in range(64):
        nums, pos, skip = knot_hash(nums, pos, skip, lengths)

    dense = []
    for i in range(0, 256, 16):
        val = 0
        for v in nums[i:i+16]:
            val = val ^ v
        dense.append(val)

    answer = ''
    for sect in dense:
        answer += hex(sect)[2:].zfill(2)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 10)
part1(INPUT)
part2(INPUT)
