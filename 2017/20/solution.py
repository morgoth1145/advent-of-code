import collections

import lib.aoc

def add_vectors(v0, v1):
    x0, y0, z0 = v0
    x1, y1, z1 = v1

    return x0+x1, y0+y1, z0+z1

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

    def step(self):
        self.vel = add_vectors(self.vel, self.acc)
        self.pos = add_vectors(self.pos, self.vel)

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
    particles = list(parse_input(s))

    turns_since_collisions = 0

    while turns_since_collisions < 1000:
        pos_counts = collections.Counter()

        for p in particles:
            p.step()
            pos_counts[p.pos] += 1

        old_size = len(particles)

        particles = [p
                     for p in particles
                     if pos_counts[p.pos] == 1]

        if old_size > len(particles):
            # Collision
            turns_since_collisions = 0
        else:
            turns_since_collisions += 1

    answer = len(particles)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 20)
part1(INPUT)
part2(INPUT)
