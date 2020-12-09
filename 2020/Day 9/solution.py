import helpers.input

def valid_check(preamble, n):
    for idx, a in enumerate(preamble):
        for b in preamble[idx+1:]:
            if a+b == n:
                return True
    return False

def part1(s):
    nums = list(map(int, s.split()))
    preamble = nums[:25]
    rest = nums[25:]
    for n in rest:
        if not valid_check(preamble, n):
            answer = n
            break
        preamble = preamble[1:] + [n]
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 9)

part1(INPUT)
part2(INPUT)
