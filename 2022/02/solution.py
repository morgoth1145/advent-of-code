import lib.aoc

def part1(s):
    SCORES = {
        'A X': 4, 'A Y': 8, 'A Z': 3,
        'B X': 1, 'B Y': 5, 'B Z': 9,
        'C X': 7, 'C Y': 2, 'C Z': 6,
    }

    answer = sum(map(SCORES.get, s.splitlines()))

    lib.aoc.give_answer(2022, 2, 1, answer)

def part2(s):
    SCORES = {
        'A X': 3, 'A Y': 4, 'A Z': 8,
        'B X': 1, 'B Y': 5, 'B Z': 9,
        'C X': 2, 'C Y': 6, 'C Z': 7,
    }

    answer = sum(map(SCORES.get, s.splitlines()))

    lib.aoc.give_answer(2022, 2, 2, answer)

INPUT = lib.aoc.get_input(2022, 2)
part1(INPUT)
part2(INPUT)
