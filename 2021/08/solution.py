import lib.aoc

def parse(s):
    for line in s.splitlines():
        start, end = line.split(' | ')
        start = [''.join(sorted(set(i))) for i in start.split()]
        end = [''.join(sorted(set(o))) for o in end.split()]
        yield start, end

def part1(s):
    answer = 0
    for _, outputs in parse(s):
        for pattern in outputs:
            if len(pattern) in (2, 3, 4, 7):
                answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 8)
part1(INPUT)
part2(INPUT)
