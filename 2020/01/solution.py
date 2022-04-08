import lib.aoc

def part1(s):
    nums = list(map(int, s.split()))
    for a in nums:
        for b in nums:
            if a + b == 2020:
                answer = a * b
                lib.aoc.give_answer(2020, 1, 1, answer)
                return

def part2(s):
    nums = list(map(int, s.split()))
    for a in nums:
        for b in nums:
            if a + b >= 2020:
                continue
            for c in nums:
                if a + b + c == 2020:
                    answer = a * b * c
                    lib.aoc.give_answer(2020, 1, 2, answer)
                    return

INPUT = lib.aoc.get_input(2020, 1)
part1(INPUT)
part2(INPUT)
