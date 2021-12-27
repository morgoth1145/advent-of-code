import lib.aoc

def part1(s):
    answer = s.count('(') - s.count(')')

    print(f'The answer to part one is {answer}')

def part2(s):
    floor = 0

    for idx, c in enumerate(s):
        if c == '(':
            floor += 1
        else:
            floor -= 1
        if floor < 0:
            answer = idx+1
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 1)
part1(INPUT)
part2(INPUT)
