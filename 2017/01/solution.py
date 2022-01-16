import lib.aoc

def part1(s):
    nums = list(map(int, s))

    answer = 0

    for a, b in zip(nums, nums[1:] + [nums[0]]):
        if a == b:
            answer += a

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 1)
part1(INPUT)
part2(INPUT)
