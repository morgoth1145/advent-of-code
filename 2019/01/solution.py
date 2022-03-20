import lib.aoc

def part1(s):
    answer = sum(max(0, m // 3 - 2)
                 for m in map(int, s.splitlines()))

    print(f'The answer to part one is {answer}')

def part2(s):
    def recursive_fuel_cost(m):
        fuel = max(0, m // 3 - 2)
        if fuel:
            fuel += recursive_fuel_cost(fuel)
        return fuel

    answer = sum(map(recursive_fuel_cost, map(int, s.splitlines())))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 1)
part1(INPUT)
part2(INPUT)
