import functools

import lib.aoc
import lib.lazy_dict

def parse_input(s):
    depth, target = s.splitlines()
    depth = int(depth.split()[1])
    x, y = target.split()[1].split(',')

    return depth, int(x), int(y)

def part1(s):
    depth, tx, ty = parse_input(s)

    MOD = 20183

    @functools.cache
    def erosion_level(x, y):
        if (x, y) in [(0, 0), (tx, ty)]:
            return 0
        if y == 0:
            return (x * 16807 + depth) % MOD
        if x == 0:
            return (y * 48271 + depth) % MOD
        return (erosion_level(x-1, y) * erosion_level(x, y-1) + depth) % MOD

    def risk_level(x, y):
        return erosion_level(x, y) % 3

    answer = sum(risk_level(x, y)
                 for x in range(tx+1)
                 for y in range(ty+1))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 22)
part1(INPUT)
part2(INPUT)
