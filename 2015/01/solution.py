import lib.aoc

def part1(s):
    floor = 0

    for c in s:
        if c == '(':
            floor += 1
        else:
            floor -= 1

    answer = floor

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 1)
part1(INPUT)
part2(INPUT)
