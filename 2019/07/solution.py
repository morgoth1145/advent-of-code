import itertools

import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    answer = 0

    for phases in itertools.permutations(range(5)):
        signal = 0
        for p in phases:
            in_chan, out_chan = intcode.Program(s).run()
            in_chan.send(p)
            in_chan.send(signal)
            signal = out_chan.recv()
        answer = max(answer, signal)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 7)
part1(INPUT)
part2(INPUT)
