import functools

import lib.aoc

def parse_input(s):
    groups = s.split('\n\n')

    a = groups[0].split(', ')
    return a, groups[1].splitlines()

def part1(s):
    a, b = parse_input(s)

    @functools.cache
    def is_match(remaining):
        if len(remaining) == 0:
            return True

        for prefix in a:
            if remaining.startswith(prefix):
                if is_match(remaining[len(prefix):]):
                    return True

        return False

    answer = 0

    for design in b:
        if is_match(design):
            answer += 1

    lib.aoc.give_answer(2024, 19, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 19)
part1(INPUT)
part2(INPUT)
