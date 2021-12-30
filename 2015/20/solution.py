import collections

import lib.aoc

def solve(s, target, present_mult, visit_limit=None):
    visiting_elves = collections.defaultdict(list)

    house = 0

    while True:
        house += 1

        visiting_elves[house].append(house)

        visiting = visiting_elves.pop(house)

        delivered = sum(visiting) * present_mult
        if delivered >= target:
            return house

        for elf in visiting:
            next_house = house + elf
            if visit_limit is not None and elf * visit_limit < next_house:
                continue
            visiting_elves[next_house].append(elf)

def part1(s):
    answer = solve(s, int(s), 10)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, int(s), 11, 50)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 20)
part1(INPUT)
part2(INPUT)
