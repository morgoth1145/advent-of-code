import gmpy2
import numpy

import lib.aoc

def solve(s, iterations):
    pop = [0] * 9
    for t in map(int, s.split(',')):
        pop[t] += 1

    # Matrices are faster (due to fast exponentiation
    # and doing the work down in C!)
    m = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # Also, Python's int is slower than gmpy2.mpz for some reason
    m = numpy.matrix([list(map(gmpy2.mpz, row)) for row in m])
    m = m ** iterations

    return (m * numpy.matrix(pop).reshape((9,1))).sum()

def part1(s):
    answer = solve(s, 80)
    lib.aoc.give_answer(2021, 6, 1, answer)

def part2(s):
    answer = solve(s, 256)
    lib.aoc.give_answer(2021, 6, 2, answer)

INPUT = lib.aoc.get_input(2021, 6)
part1(INPUT)
part2(INPUT)
