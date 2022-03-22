import threading

import lib.aoc
import lib.channels

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
    p = intcode.Program(s)
    p.memory[0] = 2 # Hack in some quarters!

    # Set up the channels here so that we can detect "deadlock" correctly
    in_chan = lib.channels.SyncChannel()
    out_chan = lib.channels.BufferedChannel()

    screen = {}

    # Each time there's an input request it's a "deadlock" until we
    # provide a move. But wait for the full screen to be read first!
    input_requests = lib.channels.detect_deadlock_events(2, in_chan, out_chan)
    def move_thread():
        for event in input_requests:
            # We need to input an action!
            paddle = None
            ball = None
            for (x, y), tile in screen.items():
                if tile == 3:
                    paddle = x
                elif tile == 4:
                    ball = x

            # Just move the paddle towards the ball. Simple AI
            if paddle == ball:
                in_chan.send(0) # Neutral
            elif paddle < ball:
                in_chan.send(1) # Right
            else:
                in_chan.send(-1) # Left

    threading.Thread(target=move_thread).start()

    p.run(in_chan, out_chan)

    score = None

    for x in out_chan:
        y = out_chan.recv()
        tile = out_chan.recv()

        if x == -1 and y == 0:
            score = tile
        else:
            screen[x,y] = tile

    # Tell the move thread to close
    input_requests.close()
    answer = score

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 13)
part1(INPUT)
part2(INPUT)
