import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split()
        yield a, b

SCORES = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

RESULTS = {
    'AX': 3,
    'BY': 3,
    'CZ': 3,
    'AY': 6,
    'BZ': 6,
    'CX': 6,
}

def part1(s):
    answer = 0

    for a, b in parse_input(s):
        answer += SCORES[b] + RESULTS.get(a+b, 0)

    lib.aoc.give_answer(2022, 2, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 2)
part1(INPUT)
part2(INPUT)
