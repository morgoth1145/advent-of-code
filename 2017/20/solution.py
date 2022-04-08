import collections

import lib.aoc
import lib.math

class Particle:
    def __init__(self, pos, vel, acc):
        formulae = []
        for i in range(3):
            a = acc[i]/2
            b = vel[i] + acc[i]/2
            c = pos[i]
            formulae.append(lib.math.Quadratic(a, b, c))

        self.x_form = formulae[0]
        self.y_form = formulae[1]
        self.z_form = formulae[2]

    def pos_at(self, t):
        return self.x_form(t), self.y_form(t), self.z_form(t)

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
        yield Particle(p, v, a)

def part1(s):
    particles = list(parse_input(s))

    long_term_manhattan_dist_formulae = []
    for p in particles:
        components = [p.x_form, p.y_form, p.z_form]
        # Flip component formulae if necessary
        # That is, this component eventually resides in the negative axis
        for idx, f in enumerate(components):
            if f.a > 0:
                # Acceleration towards positive, leave alone
                continue
            if f.a == 0:
                # Not accelerating, look at velocity
                if f.b > 0:
                    # Drifting towards positive, leave alone
                    continue
                if f.b == 0:
                    # Not moving, look at position
                    if f.c >= 0:
                        # Sitting in positive, leave alone
                        continue
            components[idx] = -components[idx]
        x, y, z = components
        long_term_manhattan_dist_formulae.append(x + y + z)

    # Select the manhattan distance formula which grows the slowest
    # The slowest growing formula will minimize the quadratic, linear, and
    # constant terms in that order
    answer = min(range(len(particles)),
                 key=lambda idx: long_term_manhattan_dist_formulae[idx].terms)

    lib.aoc.give_answer(2017, 20, 1, answer)

def part2(s):
    particles = list(parse_input(s))

    # Find potential collision times based on x
    times = set()

    for idx, p0 in enumerate(particles):
        for p1 in particles[idx+1:]:
            f = p0.x_form - p1.x_form
            times.update(t for t in f.integral_solutions()
                         if t >= 0)

    # Check for collisions at all candidate times
    for t in sorted(times):
        pos_to_indices = collections.defaultdict(list)

        for idx, p in enumerate(particles):
            pos_to_indices[p.pos_at(t)].append(idx)

        to_remove = set()

        for indices in pos_to_indices.values():
            if len(indices) > 1:
                to_remove.update(indices)

        particles = [p
                     for idx, p in enumerate(particles)
                     if idx not in to_remove]

    answer = len(particles)

    lib.aoc.give_answer(2017, 20, 2, answer)

INPUT = lib.aoc.get_input(2017, 20)
part1(INPUT)
part2(INPUT)
