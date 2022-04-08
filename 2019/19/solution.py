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

    lib.aoc.give_answer(2019, 19, 1, answer)

def part2(s):
    p = intcode.Program(s)

    def is_affected(x, y):
        in_chan, out_chan = p.clone().run()
        in_chan.send(x)
        in_chan.send(y)

        return out_chan.recv() == 1

    x, y = 0, 0

    WIDTH = 100
    HEIGHT = 100

    while True:
        # Walk down until the right side of the box is affected
        while not is_affected(x+WIDTH-1, y):
            y += 1

        # Walk right until the left side of the box is affected
        while not is_affected(x, y+HEIGHT-1):
            x += 1

        if not is_affected(x+WIDTH-1, y):
            # The right side isn't affected anymore!
            continue

        # Sanity check the full square
        assert(all(is_affected(x+dx, y+dy)
                   for dx in range(WIDTH)
                   for dy in range(HEIGHT)))
        break

    answer = 10000 * x + y

    lib.aoc.give_answer(2019, 19, 2, answer)

INPUT = lib.aoc.get_input(2019, 19)
part1(INPUT)
part2(INPUT)
