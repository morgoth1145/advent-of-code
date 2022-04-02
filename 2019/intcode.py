import threading

import lib.channels

class Program:
    def __init__(self, s):
        self.memory = list(map(int, s.split(',')))

    def clone(self):
        p = Program('1')
        p.memory = list(self.memory)
        return p

    def run(self, in_chan=None, out_chan=None,
            stop_on_no_input=False, stop_on_closed_output=False):
        if in_chan is None:
            in_chan = lib.channels.BufferedChannel()
        if out_chan is None:
            out_chan = lib.channels.BufferedChannel()
        threading.Thread(target=self.__run,
                         args=(in_chan, out_chan,
                               stop_on_no_input, stop_on_closed_output)).start()
        return in_chan, out_chan

    def __run(self, in_chan, out_chan,
              stop_on_no_input, stop_on_closed_output):
        idx = 0
        relative_base = 0

        def params(modes, n, output=False):
            nonlocal idx

            vals = self.memory[idx:idx+n]
            idx += n

            for i, v in enumerate(vals):
                modes, m = divmod(modes, 10)

                # TODO: Perhaps Python 10 pattern matching would be faster?
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
                pos = self.memory[idx]
                idx += 1

                # TODO: Perhaps Python 10 pattern matching would be faster?
                out_mode = modes % 10
                if out_mode == 0:
                    # Position mode, leave alone
                    pass
                elif out_mode == 2:
                    # Relative mode, get the absolute position
                    pos += relative_base
                else:
                    print(f'Invalid output parameter mode: {out_mode}')
                    assert(False)

                # Ensure we have room for the output
                if pos >= len(self.memory):
                    self.memory += [0] * (pos - len(self.memory) + 1)

                vals.append(pos)

            return vals

        while True:
            code = self.memory[idx]
            idx += 1

            modes, opcode = divmod(code, 100)

            if opcode == 1:
                a, b, dest = params(modes, 2, output=True)
                self.memory[dest] = a + b
                continue
            if opcode == 2:
                a, b, dest = params(modes, 2, output=True)
                self.memory[dest] = a * b
                continue
            if opcode == 3:
                dest, = params(modes, 0, output=True)
                try:
                    val = in_chan.recv()
                except lib.channels.ChannelClosed:
                    if stop_on_no_input:
                        break
                    raise
                self.memory[dest] = val
                continue
            if opcode == 4:
                val, = params(modes, 1)
                try:
                    out_chan.send(val)
                except lib.channels.ChannelClosed:
                    if stop_on_closed_output:
                        break
                    raise
                continue
            if opcode == 5:
                test, dest_idx = params(modes, 2)
                if test != 0:
                    idx = dest_idx
                continue
            if opcode == 6:
                test, dest_idx = params(modes, 2)
                if test == 0:
                    idx = dest_idx
                continue
            if opcode == 7:
                a, b, dest = params(modes, 2, output=True)
                self.memory[dest] = 1 if a < b else 0
                continue
            if opcode == 8:
                a, b, dest = params(modes, 2, output=True)
                self.memory[dest] = 1 if a == b else 0
                continue
            if opcode == 9:
                a, = params(modes, 1)
                relative_base += a
                continue
            if opcode == 99:
                break
            assert(False)

        out_chan.close()
