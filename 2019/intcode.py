class Program:
    def __init__(self, s):
        self.memory = list(map(int, s.split(',')))

    def run(self):
        idx = 0

        def take_num():
            nonlocal idx
            val = self.memory[idx]
            idx += 1
            return val

        def take_num_by_ref():
            nonlocal idx
            ref = self.memory[idx]
            idx += 1
            return self.memory[ref]

        while True:
            opcode = take_num()
            if opcode == 1:
                a = take_num_by_ref()
                b = take_num_by_ref()
                c = take_num()
                self.memory[c] = a + b
                continue
            if opcode == 2:
                a = take_num_by_ref()
                b = take_num_by_ref()
                c = take_num()
                self.memory[c] = a * b
                continue
            if opcode == 99:
                return
            assert(False)
