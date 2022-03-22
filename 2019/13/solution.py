import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    in_chan, out_chan = intcode.Program(s).run()

    screen = {}

    for x in out_chan:
        y = out_chan.recv()
        tile = out_chan.recv()

        screen[x,y] = tile

    answer = sum(1 for tile in screen.values()
                 if tile == 2)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 13)
part1(INPUT)
part2(INPUT)
