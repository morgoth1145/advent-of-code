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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 7)
part1(INPUT)
part2(INPUT)
