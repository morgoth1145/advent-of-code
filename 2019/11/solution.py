import lib.aoc
import lib.math

intcode = __import__('2019.intcode').intcode

def get_painted_grid(s):
    in_chan, out_chan = intcode.Program(s).run()

    grid = {}

    # NOTE: Low y is negative
    x, y = 0, 0
    dx, dy = 0, -1

    # Initial panel
    in_chan.send(0)

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
    grid = get_painted_grid(s)

    answer = len(grid)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 11)
part1(INPUT)
part2(INPUT)
