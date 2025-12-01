import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        c = line[0]
        n = int(line[1:])
        yield c, n

def part1(s):
    data = parse_input(s)

    pos = 50

    answer = 0

    for d, n in data:
        if d == 'R':
            pos += n
        elif d == 'L':
            pos -= n
        else:
            assert(False)
        pos = pos % 100

        if pos == 0:
            answer += 1

    lib.aoc.give_answer(2025, 1, 1, answer)

def part2(s):
    data = parse_input(s)

    pos = 50

    answer = 0

    for d, n in data:
        if d == 'R':
            d = 1
        elif d == 'L':
            d = -1
        else:
            assert(False)

        for _ in range(n):
            pos = (pos + d) % 100
            if pos == 0:
                answer += 1

    lib.aoc.give_answer(2025, 1, 2, answer)

INPUT = lib.aoc.get_input(2025, 1)
part1(INPUT)
part2(INPUT)
