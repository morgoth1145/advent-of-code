import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split(',')
        a0, a1 = tuple(map(int, a.split('-')))
        b0, b1 = tuple(map(int, b.split('-')))

        yield range(a0, a1+1), range(b0, b1+1)

def part1(s):
    answer = sum(1
                 for a, b in parse_input(s)
                 if all(i in b for i in a) or all(i in a for i in b))

    lib.aoc.give_answer(2022, 4, 1, answer)

def part2(s):
    answer = sum(1
                 for a, b in parse_input(s)
                 if any(i in b for i in a))

    lib.aoc.give_answer(2022, 4, 2, answer)

INPUT = lib.aoc.get_input(2022, 4)
part1(INPUT)
part2(INPUT)
