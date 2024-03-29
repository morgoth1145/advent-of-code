import lib.aoc

def part1(s):
    answer = 0

    for line in s.splitlines():
        nums = list(map(int, line.split()))

        answer += max(nums) - min(nums)

    lib.aoc.give_answer(2017, 2, 1, answer)

def part2(s):
    answer = 0

    for line in s.splitlines():
        nums = list(map(int, line.split()))

        for a in nums:
            for b in nums:
                if a % b == 0 and a != b:
                    answer += a // b

    lib.aoc.give_answer(2017, 2, 2, answer)

INPUT = lib.aoc.get_input(2017, 2)
part1(INPUT)
part2(INPUT)
