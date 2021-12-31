import itertools

import lib.aoc

def good_groupings(packages, target_sum, take):
    for group in itertools.combinations(packages, take):
        if sum(group) == target_sum:
            yield group # Just assume the rest can be split evenly

def entanglement(group):
    val = 1
    for p in group:
        val *= p
    return val

def part1(s):
    packages = list(map(int, s.splitlines()))

    take = 0
    while True:
        take += 1
        options = list(good_groupings(packages, sum(packages)//3, take))
        if options:
            answer = min(map(entanglement, options))
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    packages = list(map(int, s.splitlines()))

    take = 0
    while True:
        take += 1
        options = list(good_groupings(packages, sum(packages)//4, take))
        if options:
            answer = min(map(entanglement, options))
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 24)
part1(INPUT)
part2(INPUT)
