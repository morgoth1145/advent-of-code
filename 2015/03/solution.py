import lib.aoc

MOVES = {
    '>': 1,
    '<': -1,
    '^': 1j,
    'v': -1j
}

def part1(s):
    seen = {0}

    p = 0

    for c in s:
        p += MOVES[c]
        seen.add(p)

    answer = len(seen)

    lib.aoc.give_answer(2015, 3, 1, answer)

def part2(s):
    seen = {0}

    a, b = 0, 0

    for c in s:
        a += MOVES[c]
        seen.add(a)
        a, b = b, a

    answer = len(seen)

    lib.aoc.give_answer(2015, 3, 2, answer)

INPUT = lib.aoc.get_input(2015, 3)
part1(INPUT)
part2(INPUT)
