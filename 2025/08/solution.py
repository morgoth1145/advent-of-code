import heapq
import math

import lib.aoc

class CircuitGraph:
    def __init__(self, s):
        self.__coords = list(tuple(map(int, l.split(',')))
                            for l in s.splitlines())
        # Disjoint-set data structure
        # https://en.wikipedia.org/wiki/Disjoint-set_data_structure
        # TODO: Implement a proper type for this, it's come up before
        self.__circuits = list(range(len(self.__coords))) # x->x
        self.__circuit_sizes = [1] * len(self.__coords)
        self.__next_to_connect = []

        for i, c in enumerate(self.__coords):
            for j, c2 in enumerate(self.__coords[i+1:], start=i+1):
                self.__next_to_connect.append((math.dist(c, c2), i, j))

        heapq.heapify(self.__next_to_connect)

    def __circuit_find(self, x):
        xp = self.__circuits[x]
        if xp == x:
            return x
        xp = self.__circuit_find(xp)
        self.__circuits[x] = xp
        return xp

    def __circuit_mix(self, x, y):
        xp = self.__circuit_find(x)
        yp = self.__circuit_find(y)
        if xp != yp:
            self.__circuits[xp] = yp
            self.__circuit_sizes[yp] += self.__circuit_sizes[xp]
            self.__circuit_sizes[xp] = 0

    def make_connection(self):
        d, i, j = heapq.heappop(self.__next_to_connect)

        self.__circuit_mix(i, j)
        return self.__coords[i], self.__coords[j]

    def get_circuit_sizes(self):
        return [s for s in self.__circuit_sizes if s > 0]

    def is_single_circuit(self):
        return self.__circuit_sizes[self.__circuit_find(0)] == len(self.__coords)

def part1(s):
    cg = CircuitGraph(s)

    for _ in range(1000):
        cg.make_connection()

    circuit_sizes = cg.get_circuit_sizes()
    circuit_sizes.sort()

    answer = circuit_sizes[-1] * circuit_sizes[-2] * circuit_sizes[-3]

    lib.aoc.give_answer(2025, 8, 1, answer)

def part2(s):
    cg = CircuitGraph(s)

    while True:
        (x, _, _), (x2, _, _) = cg.make_connection()
        if cg.is_single_circuit():
            answer = x*x2
            break

    lib.aoc.give_answer(2025, 8, 2, answer)

INPUT = lib.aoc.get_input(2025, 8)
part1(INPUT)
part2(INPUT)
