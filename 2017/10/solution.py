import lib.aoc

def part1(s):
    nums = list(range(256))
    pos = 0
    skip = 0
    lengths = list(map(int, s.split(',')))

    for l in lengths:
        # Reverse
        to_rev = []
        for i in range(l):
            to_rev.append(nums[(pos + i) % len(nums)])
        for i, v in enumerate(to_rev[::-1]):
            nums[(pos + i) % len(nums)] = v

        pos = (pos + l + skip) % len(nums)
        skip += 1

    answer = nums[0] * nums[1]

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 10)
part1(INPUT)
part2(INPUT)
