import math

import lib.aoc

class Map:
    def __init__(self, s):
        inst, network = s.split('\n\n')
        self.inst = [c == 'R' for c in inst] # True == 1

        self.net = {}

        # These just get in the way of parsing
        network = network.replace('(', '').replace(')', '')

        for line in network.splitlines():
            node, fork = line.split(' = ')
            self.net[node] = fork.split(', ')

    def count_steps(self, pos, end_fn):
        steps = 0

        while True:
            for side in self.inst:
                steps += 1
                pos = self.net[pos][side]
                if end_fn(pos):
                    return steps

    @property
    def nodes(self):
        return self.net.keys()

def part1(s):
    answer = Map(s).count_steps('AAA', lambda pos: pos == 'ZZZ')

    lib.aoc.give_answer(2023, 8, 1, answer)

def part2(s):
    # TODO: Solve the generic problem
    # That likely requires something like lib.math.chinese_remainder_incongruence
    m = Map(s)

    # Wait, this is right?! That's hilarous!
    answer = math.lcm(*(m.count_steps(pos, lambda pos: pos[-1] == 'Z')
                        for pos in m.nodes
                        if pos[-1] == 'A'))

    lib.aoc.give_answer(2023, 8, 2, answer)

INPUT = lib.aoc.get_input(2023, 8)
part1(INPUT)
part2(INPUT)
