import lib.aoc
import lib.math

def part1(s):
    positions = list(map(int, s.split(',')))

    def value_fn(target):
        return sum(abs(p-target) for p in positions)

    target = lib.math.find_continuous_curve_minimum(range(min(positions),
                                                          max(positions)+1),
                                                    value_fn)
    answer = value_fn(target)

    print(f'The answer to part one is {answer}')

def tri_num(n):
    return n*(n+1)//2

def part2(s):
    positions = list(map(int, s.split(',')))

    def value_fn(target):
        return sum(tri_num(abs(p-target)) for p in positions)

    target = lib.math.find_continuous_curve_minimum(range(min(positions),
                                                          max(positions)+1),
                                                    value_fn)
    answer = value_fn(target)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 7)
part1(INPUT)
part2(INPUT)
