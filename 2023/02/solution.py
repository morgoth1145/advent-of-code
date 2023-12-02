import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        left, right = line.split(':')
        n = int(left.split()[1])

        bits = right.split(';')
        parsed_bits = []
        for b in bits:
            b = b.split(',')
            b = [i.split() for i in b]
            b = [(int(a), color) for a, color in b]
            parsed_bits.append(tuple(b))

        yield n, parsed_bits

def part1(s):
    data = list(parse_input(s))

    answer = 0

    LIMITS = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    for game_n, game in data:
        color_reveals = collections.Counter()

        for group in game:
            for count, color in group:
                color_reveals[color] = max(count, color_reveals[color])

        good = True

        for color, count in color_reveals.items():
            if count > LIMITS.get(color, 0):
                good = False
                break

        if good:
            answer += game_n

    lib.aoc.give_answer(2023, 2, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 2)
part1(INPUT)
part2(INPUT)
