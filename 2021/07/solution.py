import lib.aoc

def part1(s):
    positions = list(map(int, s.split(',')))
    answer = min(sum(abs(p-t) for p in positions)
                 for t in range(min(positions), max(positions)+1))

    print(f'The answer to part one is {answer}')

def tri_num(n):
    return n*(n+1)//2

def part2(s):
    positions = list(map(int, s.split(',')))
    answer = min(sum(tri_num(abs(p-t)) for p in positions)
                 for t in range(min(positions), max(positions)+1))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 7)
part1(INPUT)
part2(INPUT)
