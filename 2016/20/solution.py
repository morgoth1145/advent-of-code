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
    answer = 0
    maybe_allowed = 0

    for low, high in sorted(parse_input(s)):
        if maybe_allowed < low:
            answer += low - maybe_allowed
        maybe_allowed = max(maybe_allowed, high+1)

    answer += 4294967296 - maybe_allowed

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 20)
part1(INPUT)
part2(INPUT)
