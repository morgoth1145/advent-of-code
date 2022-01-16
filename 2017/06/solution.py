import lib.aoc

def step(nums):
    idx = nums.index(max(nums))
    new = list(nums)
    new[idx] = 0
    for i in range(nums[idx]):
        new[(idx+i+1) % len(nums)] += 1
    return tuple(new)

def part1(s):
    nums = tuple(map(int, s.split()))

    seen = {nums}

    while True:
        nums = step(nums)
        if nums in seen:
            answer = len(seen)
            break
        seen.add(nums)

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = tuple(map(int, s.split()))

    seen_steps = {
        nums: 0
    }

    while True:
        nums = step(nums)
        if nums in seen_steps:
            answer = len(seen_steps) - seen_steps[nums]
            break
        seen_steps[nums] = len(seen_steps)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 6)
part1(INPUT)
part2(INPUT)
