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
    answer = 0

    for phases in itertools.permutations(range(5, 10)):
        first_in = None
        last_out = None

        for p in phases:
            in_chan, out_chan = intcode.Program(s).run(in_chan=last_out)
            # The previous program won't output until we give it the input
            # signal. There's no chance of synchronization problems here.
            in_chan.send(p)
            if first_in is None:
                first_in = in_chan
            last_out = out_chan

        # Seed the chain
        first_in.send(0)

        for signal in last_out:
            first_in.send(signal)

        # This is the final signal
        answer = max(answer, signal)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 7)
part1(INPUT)
part2(INPUT)
