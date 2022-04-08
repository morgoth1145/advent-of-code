import threading

import lib.aoc
import lib.channels

def execute(s, pid, send_chan, recv_chan):
    def impl():
        instructions = []

        for line in s.splitlines():
            parts = line.split()
            for i in range(1, len(parts)):
                if parts[i] not in 'abcdefghijklmnopqrstuvwxyz':
                    parts[i] = int(parts[i])
            instructions.append(parts)

        idx = 0
        registers = {
            'p': pid
        }

        def get_val(val):
            if isinstance(val, int):
                return val
            return registers.get(val, 0)

        while True:
            inst = instructions[idx]

            if inst[0] == 'snd':
                send_chan.send(get_val(inst[1]))
            elif inst[0] == 'set':
                registers[inst[1]] = get_val(inst[2])
            elif inst[0] == 'add':
                registers[inst[1]] = get_val(inst[1]) + get_val(inst[2])
            elif inst[0] == 'mul':
                registers[inst[1]] = get_val(inst[1]) * get_val(inst[2])
            elif inst[0] == 'mod':
                registers[inst[1]] = get_val(inst[1]) % get_val(inst[2])
            elif inst[0] == 'rcv':
                try:
                    if recv_chan is None:
                        # Part 1 mode
                        if get_val(inst[1]):
                            send_chan.close()
                            return
                    else:
                        # Part 2 mode
                        registers[inst[1]] = recv_chan.recv()
                except lib.channels.ChannelClosed:
                    return
            elif inst[0] == 'jgz':
                if get_val(inst[1]) > 0:
                    idx += get_val(inst[2])
                    continue
            else:
                assert(False)

            idx += 1
    threading.Thread(target=impl).start()

def part1(s):
    frequencies = lib.channels.SyncChannel()
    execute(s, 0, frequencies, None)

    answer = 0
    for val in frequencies:
        answer = val

    lib.aoc.give_answer(2017, 18, 1, answer)

def part2(s):
    a_chan = lib.channels.BufferedChannel()
    b_chan = lib.channels.BufferedChannel()

    stats = lib.channels.record_message_stats(b_chan)

    deadlock_events = lib.channels.detect_deadlock_events(2, a_chan, b_chan)

    execute(s, 0, a_chan, b_chan)
    execute(s, 1, b_chan, a_chan)

    deadlock_events.recv()

    # Tell the worker threads to close
    a_chan.close()
    b_chan.close()

    answer = stats.sends

    lib.aoc.give_answer(2017, 18, 2, answer)

INPUT = lib.aoc.get_input(2017, 18)
part1(INPUT)
part2(INPUT)
