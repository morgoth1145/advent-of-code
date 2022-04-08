import lib.aoc

def part1(s):
    nums = list(map(int, s))

    answer = 0

    for a, b in zip(nums, nums[1:] + [nums[0]]):
        if a == b:
            answer += a

    lib.aoc.give_answer(2017, 1, 1, answer)

def part2(s):
    nums = list(map(int, s))

    rotated = nums[len(nums)//2:] + nums[:len(nums)//2]

    answer = 0

    for a, b in zip(nums, rotated):
        if a == b:
            answer += a

    lib.aoc.give_answer(2017, 1, 2, answer)

INPUT = lib.aoc.get_input(2017, 1)
part1(INPUT)
part2(INPUT)
