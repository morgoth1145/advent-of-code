import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split()))

def part1(s):
    data = parse_input(s)

    answer = 0

    for line in data:
        safe = True
        if line[1] > line[0]:
            for a, b in zip(line, line[1:]):
                if not (1 <= b-a <= 3):
                    safe = False
        else:
            for a, b in zip(line, line[1:]):
                if not (1 <= a-b <= 3):
                    safe = False
        if safe:
            answer += 1

    lib.aoc.give_answer(2024, 2, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 2)
part1(INPUT)
part2(INPUT)
