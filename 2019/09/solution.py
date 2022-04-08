import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    in_chan, out_chan = intcode.Program(s).run()

    in_chan.send(1)
    answer = list(out_chan)[-1]

    lib.aoc.give_answer(2019, 9, 1, answer)

def part2(s):
    in_chan, out_chan = intcode.Program(s).run()

    in_chan.send(2)
    answer = list(out_chan)[-1]

    lib.aoc.give_answer(2019, 9, 2, answer)

INPUT = lib.aoc.get_input(2019, 9)
part1(INPUT)
part2(INPUT)
