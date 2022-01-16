import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield line.split()

def part1(s):
    answer = 0

    for passphrase in parse_input(s):
        if len(passphrase) == len(set(passphrase)):
            answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 4)
part1(INPUT)
part2(INPUT)
