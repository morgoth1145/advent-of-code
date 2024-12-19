import functools

import lib.aoc

def parse_input(s):
    towels, designs = s.split('\n\n')

    return towels.split(', '), designs.splitlines()

def part1(s):
    towels, designs = parse_input(s)

    @functools.cache
    def is_match(remaining):
        if len(remaining) == 0:
            return True

        return any(is_match(remaining[len(prefix):])
                   for prefix in towels
                   if remaining.startswith(prefix))

    answer = sum(map(is_match, designs))

    lib.aoc.give_answer(2024, 19, 1, answer)

def part2(s):
    towels, designs = parse_input(s)

    @functools.cache
    def count_combos(remaining):
        if len(remaining) == 0:
            return 1

        return sum(count_combos(remaining[len(prefix):])
                   for prefix in towels
                   if remaining.startswith(prefix))

    answer = sum(map(count_combos, designs))

    lib.aoc.give_answer(2024, 19, 2, answer)

INPUT = lib.aoc.get_input(2024, 19)
part1(INPUT)
part2(INPUT)
