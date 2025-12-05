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
    first, second = s.split('\n\n')

    ranges = []
    for l in first.splitlines():
        a, b = l.split('-')
        r = (int(a), int(b))
        ranges.append(r)

    ranges.sort()

    answer = 0

    def add_part(a, b):
        if a <= b:
            ranges.append((a, b))

    def process(a, b):
        nonlocal answer

        for a2, b2 in ranges:
            if a2 <= b and b2 >= a:
                # Overlap
                first = (a, a2-1)
                second = (b2+1, b)
                add_part(*first)
                add_part(*second)
                return

        answer += b-a+1

    while ranges:
        process(*ranges.pop())

    lib.aoc.give_answer(2025, 5, 2, answer)

INPUT = lib.aoc.get_input(2025, 5)
part1(INPUT)
part2(INPUT)
