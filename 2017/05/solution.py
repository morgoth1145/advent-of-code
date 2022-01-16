import lib.aoc

def part1(s):
    nums = list(map(int, s.splitlines()))

    answer = 0
    idx = 0
    while idx < len(nums):
        answer += 1
        jump = nums[idx]
        nums[idx] += 1
        idx += jump

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(int, s.splitlines()))

    answer = 0
    idx = 0
    while idx < len(nums):
        answer += 1
        jump = nums[idx]
        if jump >= 3:
            nums[idx] -= 1
        else:
            nums[idx] += 1
        idx += jump

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 5)
part1(INPUT)
part2(INPUT)
