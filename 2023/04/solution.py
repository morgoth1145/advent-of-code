import collections

import lib.aoc

def parse_cards(s):
    for idx, line in enumerate(s.splitlines()):
        card, nums = line.split(': ')
        assert(card.split() == ['Card', str(idx+1)])

        winning, have = nums.split(' | ')
        num_match = len(set(map(int, winning.split())) &
                        set(map(int, have.split())))

        yield num_match

def part1(s):
    answer = sum(2 ** (num_match-1)
                 for num_match
                 in parse_cards(s)
                 if num_match > 0)

    lib.aoc.give_answer(2023, 4, 1, answer)

def part2(s):
    extra_copies = collections.Counter()
    answer = 0

    for idx, num_match in enumerate(parse_cards(s)):
        copies = 1 + extra_copies.get(idx, 0)
        answer += copies
        for win_idx in range(idx+1, idx+num_match+1):
            extra_copies[win_idx] += copies

    lib.aoc.give_answer(2023, 4, 2, answer)

INPUT = lib.aoc.get_input(2023, 4)
part1(INPUT)
part2(INPUT)
