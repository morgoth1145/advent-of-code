import lib.aoc
import lib.math

def parse_input(s):
    for line in s.splitlines():
        depth, layers = tuple(map(int, line.split(':')))
        cycle = 2 * (layers - 1)
        if cycle == 0:
            cycle = 1
        yield depth, layers, cycle

def part1(s):
    answer = 0

    for depth, layers, cycle in parse_input(s):
        if depth % cycle == 0:
            # Caught!
            answer += depth * layers

    lib.aoc.give_answer(2017, 13, 1, answer)

def part2(s):
    incongruencies = [(cycle, depth % cycle)
                      for depth, _, cycle in parse_input(s)]

    answer = lib.math.offset_chinese_remainder_incongruence(incongruencies)

    lib.aoc.give_answer(2017, 13, 2, answer)

INPUT = lib.aoc.get_input(2017, 13)
part1(INPUT)
part2(INPUT)
