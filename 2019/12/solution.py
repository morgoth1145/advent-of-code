import math

import lib.aoc
def parse_moons(s):
    for c in '<xyz=>':
        s = s.replace(c, '')

    for line in s.splitlines():
        x, y, z = list(map(int, line.split(',')))
        yield ([x, y, z], [0, 0, 0])

def step(moons):
    # Apply gravity to velocities
    for pos, vel in moons:
        for other_pos, _ in moons:
            for i, (p0, p1) in enumerate(zip(pos, other_pos)):
                if p0 < p1:
                    vel[i] += 1
                elif p0 > p1:
                    vel[i] -= 1

    # Apply velocities to positions
    for pos, vel in moons:
        for i, v in enumerate(vel):
            pos[i] += v

def energy(moon):
    pos, vel = moon

    return sum(map(abs, pos)) * sum(map(abs, vel))

def part1(s):
    moons = list(parse_moons(s))

    for _ in range(1000):
        step(moons)

    answer = sum(map(energy, moons))

    print(f'The answer to part one is {answer}')

def get_cycle_info(moons, comp_idx):
    # Isolate the component in question
    moons = [([p[comp_idx]], [v[comp_idx]])
             for p, v in moons]

    def get_state_key():
        return tuple((p[0], v[0])
                     for p, v in moons)

    step_num = 0
    states = {get_state_key(): step_num}

    while True:
        step_num += 1
        step(moons)

        key = get_state_key()
        last_seen = states.get(key)
        if last_seen is not None:
            return last_seen, step_num - last_seen

        states[key] = step_num

def part2(s):
    moons = list(parse_moons(s))

    x_off, x_cycle = get_cycle_info(moons, 0)
    y_off, y_cycle = get_cycle_info(moons, 1)
    z_off, z_cycle = get_cycle_info(moons, 2)

    assert(x_off == y_off == z_off == 0)

    answer = 1
    for val in (x_cycle, y_cycle, z_cycle):
        answer = (answer * val) // math.gcd(answer, val)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 12)
part1(INPUT)
part2(INPUT)
