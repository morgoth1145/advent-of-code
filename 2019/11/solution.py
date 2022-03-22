import lib.aoc
import lib.math
import lib.ocr

intcode = __import__('2019.intcode').intcode

def get_painted_grid(s, first_panel):
    in_chan, out_chan = intcode.Program(s).run()

    grid = {}

    # NOTE: Low y is negative
    x, y = 0, 0
    dx, dy = 0, -1

    # Initial panel
    in_chan.send(first_panel)

    for color in out_chan:
        turn = out_chan.recv()

        grid[x,y] = color

        if turn == 0:
            # Turn left
            dx, dy = dy, -dx
        else:
            # Turn right
            dx, dy = -dy, dx

        x += dx
        y += dy

        # New panel
        in_chan.send(grid.get((x, y), 0))

    return grid

def part1(s):
    answer = len(get_painted_grid(s, 0))

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = lib.ocr.parse_dict(get_painted_grid(s, 1), 1)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 11)
part1(INPUT)
part2(INPUT)
