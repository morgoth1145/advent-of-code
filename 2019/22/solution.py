import lib.aoc

class RNG:
    def __init__(self, factor, offset, mod):
        self.factor = factor
        self.offset = offset
        self.mod = mod

    def invert(self):
        # Modular inverse of factor
        new_factor = pow(self.factor, -1, self.mod)
        return RNG(new_factor,
                   new_factor * (self.mod - self.offset) % self.mod,
                   self.mod)

    def __add__(self, shift):
        assert(isinstance(shift, int))
        return RNG(self.factor,
                   (self.offset + shift) % self.mod,
                   self.mod)

    def __mul__(self, other):
        assert(isinstance(other, RNG))
        assert(self.mod == other.mod)

        return RNG((other.factor * self.factor) % self.mod,
                   (other.factor * self.offset + other.offset) % self.mod,
                   self.mod)

    def __pow__(self, power):
        if power == 0:
            return RNG(1, 0, self.mod)
        if power == 1:
            return self

        pow2 = self * self

        if power & 1:
            return (pow2 ** (power >> 1)) * self
        else:
            return pow2 ** (power >> 1)

    def __call__(self, value):
        return (self.factor * value + self.offset) % self.mod

def parse_rng(s, mod):
    rng = RNG(1, 0, mod)

    for line in s.splitlines():
        if line == 'deal into new stack':
            # Reverse
            # This is the same as dealing with increment of (mod - 1)
            # followed by a cut of 1
            rng *= RNG(mod-1, mod-1, mod)
            continue

        parts = line.split()
        if parts[0] == 'cut':
            # Adjust the offset
            cut_by = int(parts[1])

            # Cuts move to the end so the shift is negated
            shift_by = -cut_by
            if shift_by < 0:
                shift_by += mod

            rng += shift_by
            continue

        assert(line.startswith('deal with increment '))
        # Same as multiplying by a new factor
        rng *= RNG(int(parts[3]), 0, mod)
        continue

    return rng

def part1(s):
    answer = parse_rng(s, 10007)(2019)

    lib.aoc.give_answer(2019, 22, 1, answer)

def part2(s):
    super_rng = parse_rng(s, 119315717514047) ** 101741582076661

    answer = super_rng.invert()(2020)

    lib.aoc.give_answer(2019, 22, 2, answer)

INPUT = lib.aoc.get_input(2019, 22)
part1(INPUT)
part2(INPUT)
