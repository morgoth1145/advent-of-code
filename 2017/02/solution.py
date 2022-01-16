import lib.aoc

def part1(s):
    answer = 0

    for line in s.splitlines():
        nums = list(map(int, line.split()))

        answer += max(nums) - min(nums)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 2)
part1(INPUT)
part2(INPUT)
