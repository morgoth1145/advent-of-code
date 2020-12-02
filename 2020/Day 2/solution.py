import helpers.input

def part1(s):
    answer = 0
    for line in s.splitlines():
        policy, password = line.split(':')
        nums, c = policy.split()
        mint, maxt = list(map(int, nums.split('-')))
        password = password.strip()
        times = password.count(c)
        if mint <= times and times <= maxt:
            answer += 1
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 2)
part1(INPUT)
part2(INPUT)
