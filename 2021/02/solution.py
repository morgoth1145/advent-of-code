import lib.aoc

def part1(s):
    x, d = 0, 0
    for line in s.split('\n'):
        act, n = line.split()
        n = int(n)
        if act == 'forward':
            x += n
        elif act == 'down':
            d += n
        elif act == 'up':
            d -= n

    answer = x*d

    print(f'The answer to part one is {answer}')

def part2(s):
    x, d = 0, 0
    aim = 0
    for line in s.split('\n'):
        act, n = line.split()
        n = int(n)
        if act == 'forward':
            x += n
            d += aim*n
        elif act == 'down':
            aim += n
        elif act == 'up':
            aim -= n

    answer = x*d

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 2)
part1(INPUT)
part2(INPUT)
