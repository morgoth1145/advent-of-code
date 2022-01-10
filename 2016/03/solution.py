import lib.aoc

def part1(s):
    answer = 0

    for line in s.splitlines():
        a, b, c = list(map(int, line.split()))

        tot_len = a+b+c
        maxlen = max(a, b, c)
        rest_len = tot_len - maxlen
        if rest_len > maxlen:
            answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 3)
part1(INPUT)
part2(INPUT)
