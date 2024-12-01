import lib.aoc

def parse_input(s):
    a = []
    b = []

    for line in s.splitlines():
        an, bn = line.split()
        a.append(int(an))
        b.append(int(bn))

    return a, b

def part1(s):
    a, b = parse_input(s)

    answer = sum(abs(an-bn)
                 for an, bn
                 in zip(sorted(a), sorted(b)))

    lib.aoc.give_answer(2024, 1, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 1)
part1(INPUT)
part2(INPUT)
