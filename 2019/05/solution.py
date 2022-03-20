import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    in_chan, out_chan = intcode.Program(s).run()

    in_chan.send(1)
    answer = list(out_chan)[-1]

    print(f'The answer to part one is {answer}')

def part2(s):
    in_chan, out_chan = intcode.Program(s).run()

    in_chan.send(5)
    answer = out_chan.recv()

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 5)
part1(INPUT)
part2(INPUT)
