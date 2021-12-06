import collections

import lib.aoc

def iterate(pop):
    new_pop = collections.Counter()
    for t, n in pop.items():
        if t == 0:
            new_pop[6] += n
            new_pop[8] += n
        else:
            new_pop[t-1] += n
    return new_pop

def part1(s):
    pop = collections.Counter(map(int, s.split(',')))

    for _ in range(80):
        pop = iterate(pop)

    answer = sum(pop.values())

    print(f'The answer to part one is {answer}')

def part2(s):
    pop = collections.Counter(map(int, s.split(',')))

    for _ in range(256):
        pop = iterate(pop)

    answer = sum(pop.values())

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 6)
part1(INPUT)
part2(INPUT)
