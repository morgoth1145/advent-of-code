import functools
import re2 as re

import lib.aoc

def parse_input(s):
    towels, designs = s.split('\n\n')

    return towels.split(', '), designs.splitlines()

def part1(s):
    towels, designs = parse_input(s)

    r = re.compile('(?:' + '|'.join(towels) + ')*')
    answer = sum(r.fullmatch(d) is not None
                 for d in designs)

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
