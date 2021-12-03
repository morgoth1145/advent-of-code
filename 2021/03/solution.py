import lib.aoc

def part1(s):
    nums = []
    for n in s.split():
        nums.append(n)

    bits = len(s.split()[0])

    gamma = []
    epsilon = []

    for b in range(bits):
        c1 = 0
        c0 = 0
        for n in nums:
            if n[b] == '1':
                c1 += 1
            else:
                c0 += 1

        if c1 > c0:
            gamma.append('1')
            epsilon.append('0')
        else:
            gamma.append('0')
            epsilon.append('1')

    gamma = int(''.join(gamma), base=2)
    epsilon = int(''.join(epsilon), base=2)

    answer = gamma*epsilon

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 3)
part1(INPUT)
part2(INPUT)
