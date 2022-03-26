import threading

import lib.aoc
import lib.channels

intcode = __import__('2019.intcode').intcode

class Packet:
    def __init__(self, dest, x, y, nat_generated=False):
        self.dest = dest
        self.x = x
        self.y = y
        self.nat_generated = nat_generated

def read_packets_and_forward(comp_out_chan, controller_chan):
    for dest in comp_out_chan:
        x = comp_out_chan.recv()
        y = comp_out_chan.recv()

        controller_chan.send(Packet(dest, x, y))

def part1(s):
    in_channels = []
    out_channels = []

    controller_chan = lib.channels.BufferedChannel()

    # Set up channels
    for _ in range(50):
        in_channels.append(lib.channels.BufferedChannel())
        out_channels.append(lib.channels.BufferedChannel())

    # Initialize the input channels
    for addr, in_chan in enumerate(in_channels):
        in_chan.send(addr)
        # After sending useful information, pretend that there's no packet
        # waiting and send -1
        in_chan.send(-1)

    # Forward packets from each program to the controller
    for out_chan in out_channels:
        threading.Thread(target=read_packets_and_forward,
                         args=(out_chan, controller_chan)).start()

    # Start programs
    for in_chan, out_chan in zip(in_channels, out_channels):
        intcode.Program(s).run(in_chan=in_chan, out_chan=out_chan,
                               stop_on_no_input=True)

    # Controller loop
    for packet in controller_chan:
        if packet.dest == 255:
            answer = packet.y
            break
        in_chan = in_channels[packet.dest]
        in_chan.send(packet.x)
        in_chan.send(packet.y)
        # After sending useful information, pretend that there's no packet
        # waiting and send -1
        in_chan.send(-1)

    # Close all input channels to shut down the network
    for in_chan in in_channels:
        in_chan.close()

    print(f'The answer to part one is {answer}')

def part2(s):
    in_channels = []
    out_channels = []

    controller_chan = lib.channels.BufferedChannel()

    # Set up channels
    for _ in range(50):
        in_channels.append(lib.channels.BufferedChannel())
        out_channels.append(lib.channels.BufferedChannel())

    deadlock_chan = lib.channels.detect_deadlock_events(101,
                                                        controller_chan,
                                                        *(in_channels + out_channels))

    # Initialize the input channels
    for addr, in_chan in enumerate(in_channels):
        in_chan.send(addr)
        # After sending useful information, pretend that there's no packet
        # waiting and send -1
        in_chan.send(-1)

    # Forward packets from each program to the controller
    for out_chan in out_channels:
        threading.Thread(target=read_packets_and_forward,
                         args=(out_chan, controller_chan)).start()

    # Start programs
    for in_chan, out_chan in zip(in_channels, out_channels):
        intcode.Program(s).run(in_chan=in_chan, out_chan=out_chan,
                               stop_on_no_input=True)

    nat_packet = None

    def nat_listener():
        for deadlock in deadlock_chan:
            assert(nat_packet is not None)

            # Send a copy of the last nat packet to 0
            controller_chan.send(Packet(0, nat_packet.x, nat_packet.y, True))
    threading.Thread(target=nat_listener).start()

    last_nat_sent_y = None

    # Controller loop
    for msg in controller_chan:
        if msg.nat_generated:
            if msg.y == last_nat_sent_y:
                answer = msg.y
                break
            last_nat_sent_y = msg.y

        if msg.dest == 255:
            nat_packet = msg
            continue

        in_chan = in_channels[msg.dest]
        in_chan.send(msg.x)
        in_chan.send(msg.y)
        # After sending useful information, pretend that there's no packet
        # waiting and send -1
        in_chan.send(-1)
        continue

    # Close all input channels to shut down the network
    for in_chan in in_channels:
        in_chan.close()

    # And close the background deadlock listener thread
    deadlock_chan.close()

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 23)
part1(INPUT)
part2(INPUT)
