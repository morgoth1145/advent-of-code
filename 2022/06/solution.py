import lib.aoc

def part1(s):
    for i in range(len(s)):
        if len(set(s[i:i+4])) == 4:
            answer = i+4
            break

    lib.aoc.give_answer(2022, 6, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 6)
part1(INPUT)
part2(INPUT)
