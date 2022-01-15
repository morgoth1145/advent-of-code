import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split('-')
        yield int(a), int(b)

def part1(s):
    answer = 0
    for low, high in sorted(parse_input(s)):
        if answer < low:
            break
        answer = max(answer, high+1)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 20)
part1(INPUT)
part2(INPUT)
