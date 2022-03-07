import lib.aoc

class Particle:
    def __init__(self, idx, pos, vel, acc):
        self.idx = idx
        self.pos = pos
        self.vel = vel
        self.acc = acc

    @property
    def manhattan_velocity(self):
        return sum(map(abs, self.vel))

    @property
    def manhattan_acceleration(self):
        return sum(map(abs, self.acc))

    def __str__(self):
        return f'Particle({self.pos}, {self.vel}, {self.acc})'

def parse_vec(v):
    v = v[3:-1]
    return tuple(map(int, v.split(',')))

def parse_input(s):
    for idx, line in enumerate(s.splitlines()):
        p, v, a = line.split(', ')
        p = parse_vec(p)
        v = parse_vec(v)
        a = parse_vec(a)
        yield Particle(idx, p, v, a)

def part1(s):
    particles = sorted(parse_input(s),
                       key=lambda p: (p.manhattan_acceleration,
                                      p.manhattan_velocity))

    for idx in range(1, len(particles)):
        if particles[idx].manhattan_acceleration > particles[0].manhattan_acceleration:
            particles = particles[:idx]
            break

    # Assume no acceleration goes "counter" to the initial velocity
    # Assume that there is a minimum velocity for the minimum acceleration

    answer = particles[0].idx

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 20)
part1(INPUT)
part2(INPUT)
