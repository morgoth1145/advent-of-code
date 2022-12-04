import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split(',')
        a0, a1 = tuple(map(int, a.split('-')))
        b0, b1 = tuple(map(int, b.split('-')))

        yield range(a0, a1+1), range(b0, b1+1)

def part1(s):
    data = parse_input(s)

    answer = 0

    for a, b in data:
        if all(i in b for i in a) or all(i in a for i in b):
            answer += 1

    lib.aoc.give_answer(2022, 4, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 4)
part1(INPUT)
part2(INPUT)
