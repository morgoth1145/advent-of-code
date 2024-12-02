import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split()))

def test(line):
    if line[1] > line[0]:
        for a, b in zip(line, line[1:]):
            if not (1 <= b-a <= 3):
                return False
    else:
        for a, b in zip(line, line[1:]):
            if not (1 <= a-b <= 3):
                return False
    return True

def part1(s):
    data = parse_input(s)

    answer = 0

    for line in data:
        if test(line):
            answer += 1

    lib.aoc.give_answer(2024, 2, 1, answer)

def test2(line):
    if test(line):
        return True
    if any(test(line[:i] + line[i+1:])
           for i in range(len(line))):
        return True
    return False

def part2(s):
    data = parse_input(s)

    answer = 0

    for line in data:
        if test2(line):
            answer += 1

    lib.aoc.give_answer(2024, 2, 2, answer)

INPUT = lib.aoc.get_input(2024, 2)
part1(INPUT)
part2(INPUT)
