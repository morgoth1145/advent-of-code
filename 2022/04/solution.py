import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split(',')

        yield tuple(map(int, a.split('-'))), tuple(map(int, b.split('-')))

def part1(s):
    answer = sum(1
                 for (a0, a1), (b0, b1) in parse_input(s)
                 if a0 <= b0 <= b1 <= a1 or b0 <= a0 <= a1 <= b1)

    lib.aoc.give_answer(2022, 4, 1, answer)

def part2(s):
    answer = sum(1
                 for (a0, a1), (b0, b1) in parse_input(s)
                 if a0 <= b1 and a1 >= b0)

    lib.aoc.give_answer(2022, 4, 2, answer)

INPUT = lib.aoc.get_input(2022, 4)
part1(INPUT)
part2(INPUT)
