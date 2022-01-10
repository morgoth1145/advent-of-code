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

def gen_real_tris(s):
    lines = s.splitlines()
    while lines:
        a = lines.pop(0).split()
        b = lines.pop(0).split()
        c = lines.pop(0).split()

        yield int(a.pop(0)), int(b.pop(0)), int(c.pop(0))
        yield int(a.pop(0)), int(b.pop(0)), int(c.pop(0))
        yield int(a.pop(0)), int(b.pop(0)), int(c.pop(0))

def part2(s):
    answer = 0

    for a, b, c in gen_real_tris(s):

        tot_len = a+b+c
        maxlen = max(a, b, c)
        rest_len = tot_len - maxlen
        if rest_len > maxlen:
            answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 3)
part1(INPUT)
part2(INPUT)
