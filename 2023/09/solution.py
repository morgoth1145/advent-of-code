import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield list(map(int, line.split()))

def extrapolate(seq):
    if set(seq) == {0}:
        return 0

    d = extrapolate([v1-v0 for v0, v1 in zip(seq, seq[1:])])
    return seq[-1] + d

def part1(s):
    answer = sum(map(extrapolate, parse_input(s)))

    lib.aoc.give_answer(2023, 9, 1, answer)

def part2(s):
    answer = sum(extrapolate(seq[::-1]) for seq in parse_input(s))

    lib.aoc.give_answer(2023, 9, 2, answer)

INPUT = lib.aoc.get_input(2023, 9)
part1(INPUT)
part2(INPUT)
