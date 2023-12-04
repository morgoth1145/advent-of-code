import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split(': ')
        left, right = b.split(' | ')
        left = set(map(int, left.split()))
        right = set(map(int, right.split()))

        assert(a.startswith('Card '))
        a = int(a.split()[1])

        yield a, left, right

def part1(s):
    data = list(parse_input(s))

    answer = 0

    for _, winning, have in data:
        n = len(winning & have)
        if n == 0:
            continue
        answer += 2 ** (n-1)

    lib.aoc.give_answer(2023, 4, 1, answer)

def part2(s):
    data = list(parse_input(s))

    copies = [1] * len(data)

    for num, winning, have in data:
        num -= 1
        mult = copies[num]
        n = len(winning & have)
        for off in range(1, n+1):
            off = num + off
            if off >= len(copies):
                continue
            copies[off] += mult

    answer = sum(copies)

    lib.aoc.give_answer(2023, 4, 2, answer)

INPUT = lib.aoc.get_input(2023, 4)
part1(INPUT)
part2(INPUT)
