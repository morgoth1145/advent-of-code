import lib.aoc

def part1(s):
    pairs = [tuple(map(int, l.split(',')))
             for l in s.splitlines()]

    answer = 0

    for idx, (x, y) in enumerate(pairs):
        for x2, y2 in pairs[idx+1:]:
            area = (abs(x-x2)+1) * (abs(y-y2)+1)
            answer = max(answer, area)

    lib.aoc.give_answer(2025, 9, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 9)
part1(INPUT)
part2(INPUT)
