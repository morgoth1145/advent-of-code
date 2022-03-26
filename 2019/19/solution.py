import functools

import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    p = intcode.Program(s)

    answer = 0

    for x in range(50):
        for y in range(50):
            in_chan, out_chan = p.clone().run()
            in_chan.send(x)
            in_chan.send(y)

            if out_chan.recv() == 1:
                answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 19)
part1(INPUT)
part2(INPUT)
