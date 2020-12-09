import helpers.input

def valid_check(preamble, n):
    for idx, a in enumerate(preamble):
        for b in preamble[idx+1:]:
            if a+b == n:
                return True
    return False

def get_invalid_num(nums):
    preamble = nums[:25]
    rest = nums[25:]
    for n in rest:
        if not valid_check(preamble, n):
            return n
        preamble = preamble[1:] + [n]

def part1(s):
    nums = list(map(int, s.split()))
    answer = get_invalid_num(nums)
    print(f'The answer to part one is {answer}')

def partial_sums(nums):
    tot = 0
    for n in nums:
        tot += n
        yield tot

def part2(s):
    nums = list(map(int, s.split()))
    target = get_invalid_num(nums)
    sums = list(partial_sums(nums))
    for idx, a in enumerate(sums):
        for idx2, b in enumerate(sums[idx+1:]):
            diff = b - a
            if diff > target:
                break
            if diff == target:
                the_nums = nums[idx+1:idx+idx2+2]
                assert(sum(the_nums) == target)
                answer = min(the_nums) + max(the_nums)
                print(f'The answer to part two is {answer}')
                return

INPUT = helpers.input.get_input(2020, 9)

part1(INPUT)
part2(INPUT)
