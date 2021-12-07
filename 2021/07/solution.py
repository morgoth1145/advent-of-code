import functools

import lib.aoc

def calc_total_fuel(positions, target):
    return sum(abs(p-target) for p in positions)

def part1(s):
    nums = list(map(int, s.split(',')))

    best = None
    for t in range(min(nums), max(nums)+1):
        fuel = calc_total_fuel(nums, t)
        if best is None:
            best = fuel
        elif best > fuel:
            best = fuel

    answer = best

    print(f'The answer to part one is {answer}')

@functools.cache
def fuel_cost(distance):
    if distance == 0:
        return 0
    return distance + fuel_cost(distance-1)

def calc_total_fuel_2(positions, target):
    return sum(fuel_cost(abs(p-target)) for p in positions)

def part2(s):
    nums = list(map(int, s.split(',')))

    # Warm cache
    for d in range(0, max(nums)-min(nums), 10):
        _ = fuel_cost(d)

    best = None
    for t in range(min(nums), max(nums)+1):
        fuel = calc_total_fuel_2(nums, t)
        if best is None:
            best = fuel
        elif best > fuel:
            best = fuel

    answer = best

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 7)
part1(INPUT)
part2(INPUT)
