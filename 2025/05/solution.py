import lib.aoc

def part1(s):
    first, second = s.split('\n\n')

    ranges = []
    for l in first.splitlines():
        a, b = l.split('-')
        r = (int(a), int(b))
        ranges.append(r)

    answer = 0

    for n in map(int, second.splitlines()):
        good = False
        for a, b in ranges:
            if a <= n <= b:
                good = True
                break

        if good:
            answer += 1

    lib.aoc.give_answer(2025, 5, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 5)
part1(INPUT)
part2(INPUT)
