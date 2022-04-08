import threading

import lib.aoc
import lib.channels

intcode = __import__('2019.intcode').intcode

class Packet:
    def __init__(self, src, dest, x, y):
        self.src = src
        self.dest = dest
        self.x = x
        self.y = y

def run(s, num_processes, include_nat):
    NAT_ADDR = 255

    in_channels = []
    out_channels = []

    controller_chan = lib.channels.BufferedChannel()

    # Set up channels
    for _ in range(num_processes):
        in_channels.append(lib.channels.BufferedChannel())
        out_channels.append(lib.channels.BufferedChannel())

    deadlock_chan = lib.channels.detect_deadlock_events(2*num_processes+1,
                                                        controller_chan,
                                                        *(in_channels + out_channels))

    def forward_deadlocks():
        for deadlock in deadlock_chan:
            controller_chan.send('deadlock')
    threading.Thread(target=forward_deadlocks).start()

    # Initialize the input channels
    for addr, in_chan in enumerate(in_channels):
        in_chan.send(addr)

    # Forward packets from each program to the controller
    def forward_program_packets(src, out_chan):
        for dest in out_chan:
            x = out_chan.recv()
            y = out_chan.recv()

            controller_chan.send(Packet(src, dest, x, y))
    for addr, out_chan in enumerate(out_channels):
        threading.Thread(target=forward_program_packets,
                         args=(addr, out_chan)).start()

    # Start programs
    for in_chan, out_chan in zip(in_channels, out_channels):
        intcode.Program(s).run(in_chan=in_chan, out_chan=out_chan,
                               stop_on_no_input=True)

    def shutdown_network():
        for in_chan in in_channels:
            in_chan.close()

        deadlock_chan.close()

    nat_packet = None
    last_nat_generated_y = None

    active_machines = set(range(num_processes))

    # Controller loop
    for msg in controller_chan:
        if msg == 'deadlock':
            if len(active_machines) == 0:
                # Absolute deadlock!
                assert(include_nat)
                controller_chan.send(Packet(NAT_ADDR, 0, nat_packet.x, nat_packet.y))
                continue

            addr = min(active_machines)
            active_machines.remove(addr)
            in_channels[addr].send(-1)
            continue

        if msg.src == NAT_ADDR:
            assert(include_nat)
            if msg.y == last_nat_generated_y:
                # This is our first duplicate (part 2)
                shutdown_network()
                return last_nat_generated_y
            last_nat_generated_y = msg.y

        if msg.src != NAT_ADDR:
            active_machines.add(msg.src)
        if msg.dest != NAT_ADDR:
            active_machines.add(msg.dest)

        if msg.dest == NAT_ADDR:
            if include_nat:
                nat_packet = msg
            else:
                # This is the first message to the nat (part 1)
                shutdown_network()
                return msg.y
            continue

        in_chan = in_channels[msg.dest]
        in_chan.send(msg.x)
        in_chan.send(msg.y)
        continue

def part1(s):
    answer = run(s, 50, include_nat=False)

    lib.aoc.give_answer(2019, 23, 1, answer)

def part2(s):
    answer = run(s, 50, include_nat=True)

    lib.aoc.give_answer(2019, 23, 2, answer)

INPUT = lib.aoc.get_input(2019, 23)
part1(INPUT)
part2(INPUT)
