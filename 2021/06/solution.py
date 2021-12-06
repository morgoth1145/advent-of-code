import lib.aoc

def solve(s, iterations):
    pop = [0] * 9
    for t in map(int, s.split(',')):
        pop[t] += 1
    for _ in range(iterations):
        reproducing = pop[0]
        pop = pop[1:] + [reproducing]
        pop[6] += reproducing
    return sum(pop)

def part1(s):
    answer = solve(s, 80)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 256)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 6)
part1(INPUT)
part2(INPUT)
