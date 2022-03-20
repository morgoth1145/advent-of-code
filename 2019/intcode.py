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

        def params(code, n, output=False):
            nonlocal idx
            modes = code // 100

            if output:
                n += 1

            vals = self.memory[idx:idx+n]
            idx += n
            modes = list(map(int, str(modes).zfill(n)[::-1]))
            if output:
                # The output should be in position mode
                if modes[-1] != 0:
                    print(idx-1-n, code, n, output, vals, modes)
                assert(modes[-1] == 0)
                # But treat it as immediate mode so that we get the memory
                # index to store the output
                modes[-1] = 1

            for i, (v, m) in enumerate(zip(vals, modes)):
                if m == 0:
                    # Position mode
                    vals[i] = self.memory[v]
                elif m == 1:
                    # Immediate mode, leave alone
                    pass
                else:
                    print(f'Unknown parameter mode: {m}')
                    assert(False)

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
            if opcode == 99:
                out_chan.close()
                return
            assert(False)
