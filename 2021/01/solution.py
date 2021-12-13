import lib.aoc

def part1(s):
    nums = list(map(int, s.split()))
    answer = 0
    for i in range(len(nums)-1):
        if nums[i] < nums[i+1]:
            answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(int, s.split()))
    answer = 0
    for i in range(len(nums)-3):
        if nums[i] < nums[i+3]:
            answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 1)
part1(INPUT)
part2(INPUT)