import threading

import lib.channels

class Program:
    def __init__(self, s):
        self.memory = list(map(int, s.split(',')))

    def run(self, in_chan=None):
        if in_chan is None:
            in_chan = lib.channels.BufferedChannel()
        out_chan = lib.channels.BufferedChannel()
        threading.Thread(target=self.__run,
                         args=(in_chan, out_chan)).start()
        return in_chan, out_chan

    def __run(self, in_chan, out_chan):
        idx = 0
        relative_base = 0

        def params(code, n, output=False):
            nonlocal idx
            modes = code // 100

            if output:
                n += 1

            vals = self.memory[idx:idx+n]
            idx += n
            modes = list(map(int, str(modes).zfill(n)[::-1]))
            if output:
                # The output should not be in immediate mode
                assert(modes[-1] in (0, 2))
                # But store the output mode and treat it as immediate mode
                # in the main loop to leave it alone. (We want the output
                # position, not the value at that position!)
                out_mode = modes[-1]
                modes[-1] = 1

            for i, (v, m) in enumerate(zip(vals, modes)):
                if m == 0:
                    # Position mode
                    if v >= len(self.memory):
                        self.memory += [0] * (v - len(self.memory) + 1)
                    vals[i] = self.memory[v]
                elif m == 1:
                    # Immediate mode, leave alone
                    pass
                elif m == 2:
                    # Relative mode
                    v += relative_base
                    if v >= len(self.memory):
                        self.memory += [0] * (v - len(self.memory) + 1)
                    vals[i] = self.memory[v]
                else:
                    print(f'Unknown parameter mode: {m}')
                    assert(False)

            if output:
                if out_mode == 2:
                    # Output was in relative mode, get the absolute position
                    vals[-1] += relative_base
                # Ensure we have room for the output
                pos = vals[-1]
                if pos >= len(self.memory):
                    self.memory += [0] * (pos - len(self.memory) + 1)

            return vals

        while True:
            code = self.memory[idx]
            idx += 1

            opcode = code % 100

            if opcode == 1:
                a, b, dest = params(code, 2, output=True)
                self.memory[dest] = a + b
                continue
            if opcode == 2:
                a, b, dest = params(code, 2, output=True)
                self.memory[dest] = a * b
                continue
            if opcode == 3:
                dest, = params(code, 0, output=True)
                val = in_chan.recv()
                self.memory[dest] = val
                continue
            if opcode == 4:
                val, = params(code, 1)
                out_chan.send(val)
                continue
            if opcode == 5:
                test, dest_idx = params(code, 2)
                if test != 0:
                    idx = dest_idx
                continue
            if opcode == 6:
                test, dest_idx = params(code, 2)
                if test == 0:
                    idx = dest_idx
                continue
            if opcode == 7:
                a, b, dest = params(code, 2, output=True)
                self.memory[dest] = 1 if a < b else 0
                continue
            if opcode == 8:
                a, b, dest = params(code, 2, output=True)
                self.memory[dest] = 1 if a == b else 0
                continue
            if opcode == 9:
                a, = params(code, 1)
                relative_base += a
                continue
            if opcode == 99:
                out_chan.close()
                return
            assert(False)
