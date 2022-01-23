import lib.aoc

def parse_instructions(s):
    instructions = []

    for line in s.splitlines():
        parts = line.split()
        if parts[1] not in 'abcdefghijklmnopqrstuvwxyz':
            parts[1] = int(parts[1])
        if len(parts) > 2 and parts[2] not in 'abcdefghijklmnopqrstuvwxyz':
            parts[2] = int(parts[2])
        instructions.append(parts)

    return instructions

def part1(s):
    instructions = parse_instructions(s)

    idx = 0
    registers = {}
    last_frequency = None

    def get_val(val):
        if isinstance(val, int):
            return val
        return registers.get(val, 0)

    while True:
        inst = instructions[idx]

        if inst[0] == 'snd':
            last_frequency = get_val(inst[1])
        elif inst[0] == 'set':
            registers[inst[1]] = get_val(inst[2])
        elif inst[0] == 'add':
            registers[inst[1]] = get_val(inst[1]) + get_val(inst[2])
        elif inst[0] == 'mul':
            registers[inst[1]] = get_val(inst[1]) * get_val(inst[2])
        elif inst[0] == 'mod':
            registers[inst[1]] = get_val(inst[1]) % get_val(inst[2])
        elif inst[0] == 'rcv':
            x = get_val(inst[1])
            if x:
                answer = last_frequency
                break
        elif inst[0] == 'jgz':
            if get_val(inst[1]) > 0:
                idx += get_val(inst[2])
                continue
        else:
            assert(False)

        idx += 1

    print(f'The answer to part one is {answer}')

class Program:
    def __init__(self, s, pid):
        self.instructions = parse_instructions(s)
        self.idx = 0
        self.registers = {'p': pid}
        self.send_count = 0
        self.queue = []

    def push_val(self, val):
        self.queue.append(val)

    @property
    def blocked(self):
        return len(self.queue) == 0

    def _get_val(self, val):
        if isinstance(val, int):
            return val
        return self.registers.get(val, 0)

    def execute(self):
        outputs = []

        while True:
            inst = self.instructions[self.idx]

            if inst[0] == 'snd':
                outputs.append(self._get_val(inst[1]))
                self.send_count += 1
            elif inst[0] == 'set':
                self.registers[inst[1]] = self._get_val(inst[2])
            elif inst[0] == 'add':
                self.registers[inst[1]] = self._get_val(inst[1]) + self._get_val(inst[2])
            elif inst[0] == 'mul':
                self.registers[inst[1]] = self._get_val(inst[1]) * self._get_val(inst[2])
            elif inst[0] == 'mod':
                self.registers[inst[1]] = self._get_val(inst[1]) % self._get_val(inst[2])
            elif inst[0] == 'rcv':
                if len(self.queue) == 0:
                    return outputs

                self.registers[inst[1]] = self.queue.pop(0)
            elif inst[0] == 'jgz':
                if self._get_val(inst[1]) > 0:
                    self.idx += self._get_val(inst[2])
                    continue
            else:
                assert(False)

            self.idx += 1

def part2(s):
    a = Program(s, 0)
    b = Program(s, 1)

    while True:
        a_outputs = a.execute()
        for val in a_outputs:
            b.push_val(val)
        b_outputs = b.execute()
        for val in b_outputs:
            a.push_val(val)
        if a.blocked and b.blocked:
            break

    answer = b.send_count

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 18)
part1(INPUT)
part2(INPUT)
