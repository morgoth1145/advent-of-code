import numpy

import lib.aoc

def solve(s, iterations):
    pop = [0] * 9
    for t in map(int, s.split(',')):
        pop[t] += 1

    # Matrices are faster (due to fast exponentiation
    # and doing the work down in C!)
    m = numpy.matrix([
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=object)
    m = m ** iterations

    return (m * numpy.matrix(pop).reshape((9,1))).sum()

def part1(s):
    answer = solve(s, 80)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 256)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 6)
part1(INPUT)
part2(INPUT)
