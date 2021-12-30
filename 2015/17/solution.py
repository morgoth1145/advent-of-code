import itertools

import lib.aoc

def count_matching_combinations(containers, n):
    return sum(1
               for combo in itertools.combinations(containers, n)
               if sum(combo) == 150)

def part1(s):
    containers = list(map(int, s.splitlines()))

    answer = sum(count_matching_combinations(containers, n)
                 for n in range(len(containers)))

    print(f'The answer to part one is {answer}')

def part2(s):
    containers = list(map(int, s.splitlines()))

    for n in range(len(containers)):
        answer = count_matching_combinations(containers, n)
        if answer != 0:
            # This is the minimum number of containers required!
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 17)
part1(INPUT)
part2(INPUT)
