import helpers.input

def part1(s):
    nums = list(map(int, s.split()))
    for a in nums:
        for b in nums:
            if a + b == 2020:
                answer = a * b
                print(f'The answer to part one is {answer}')
                return

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 1)
part1(INPUT)
part2(INPUT)
