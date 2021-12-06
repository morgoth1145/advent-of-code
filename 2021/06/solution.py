import lib.aoc

def solve(s, iterations):
    pop = [0] * 9
    for t in map(int, s.split(',')):
        pop[t] += 1
    off = 0
    for _ in range(iterations):
        pop[off + 7 - 9] += pop[off]
        off = (off + 1) % 9
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
