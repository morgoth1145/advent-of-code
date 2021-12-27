import lib.aoc

def part1(s):
    answer = 0

    for line in s.splitlines():
        x, y, z = list(map(int, line.split('x')))
        sides = (x*y, x*z, y*z)
        slack = min(sides)
        answer += 2*sum(sides) + slack

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = 0

    for line in s.splitlines():
        x, y, z = list(map(int, line.split('x')))
        sides = (2*x+2*y, 2*x+2*z, 2*y+2*z)
        answer += min(sides) + x*y*z

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 2)
part1(INPUT)
part2(INPUT)
