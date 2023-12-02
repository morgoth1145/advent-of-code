import collections

import lib.aoc

def parse_games(s):
    for line in s.splitlines():
        left, right = line.split(':')
        n = int(left.split()[1])

        # We don't care about the rounds, just the maximum color counts!
        right = right.replace(';', ',')

        cubes = collections.Counter()

        for count in right.split(', '):
            count, color = count.split()
            cubes[color] = max(int(count), cubes[color])

        yield n, cubes

def part1(s):
    LIMITS = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    answer = sum(n
                 for n, cubes in parse_games(s)
                 if all(LIMITS[color] >= count
                        for color, count in cubes.items()))

    lib.aoc.give_answer(2023, 2, 1, answer)

def part2(s):
    answer = 0

    for _, cubes in parse_games(s):
        power = 1

        for count in cubes.values():
            power *= count

        answer += power

    lib.aoc.give_answer(2023, 2, 2, answer)

INPUT = lib.aoc.get_input(2023, 2)
part1(INPUT)
part2(INPUT)
