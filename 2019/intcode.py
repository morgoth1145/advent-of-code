import threading

import lib.channels

class Program:
    def __init__(self, s):
        self.memory = list(map(int, s.split(',')))
        self.in_chan = lib.channels.SyncChannel()
        self.out_chan = lib.channels.SyncChannel()

    def run_async(self):
        # TODO: Fix
        threading.Thread(target=self.run).start()

    def run(self):
        idx = 0

        while True:
            opcode = self.memory[idx]
            idx += 1
            modes = opcode // 100
            opcode = opcode % 100

            def take_num():
                nonlocal idx, modes
                assert(modes % 10 == 0)
                modes = modes // 10
                val = self.memory[idx]
                idx += 1
                return val

            def take_mode_num():
                nonlocal idx, modes
                m = modes % 10
                modes = modes // 10
                val = self.memory[idx]
                idx += 1
                if m == 1:
                    return val
                if m == 0:
                    return self.memory[val]
                print('Unknown mode')
                assert(False)

            if opcode == 1:
                a = take_mode_num()
                b = take_mode_num()
                c = take_num()
                self.memory[c] = a + b
                continue
            if opcode == 2:
                a = take_mode_num()
                b = take_mode_num()
                c = take_num()
                self.memory[c] = a * b
                continue
            if opcode == 3:
                val = self.in_chan.recv()
                dest = take_num()
                self.memory[dest] = val
                continue
            if opcode == 4:
                val = take_mode_num()
                self.out_chan.send(val)
                continue
            if opcode == 5:
                test = take_mode_num()
                dest = take_mode_num()
                if test != 0:
                    idx = dest
                continue
            if opcode == 6:
                test = take_mode_num()
                dest = take_mode_num()
                if test == 0:
                    idx = dest
                continue
            if opcode == 7:
                a = take_mode_num()
                b = take_mode_num()
                dest = take_num()
                self.memory[dest] = 1 if a < b else 0
                continue
            if opcode == 8:
                a = take_mode_num()
                b = take_mode_num()
                dest = take_num()
                self.memory[dest] = 1 if a == b else 0
                continue
            if opcode == 99:
                self.out_chan.close()
                return
            assert(False)
