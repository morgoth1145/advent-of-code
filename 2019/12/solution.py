import lib.aoc
import lib.math

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

    lib.aoc.give_answer(2019, 12, 1, answer)

def get_cycle_congruence(moons, comp_idx):
    # Isolate the component in question
    moons = [([p[comp_idx]], [v[comp_idx]])
             for p, v in moons]

    def state_key():
        return tuple((p[0], v[0]) for p, v in moons)

    step_num = 0
    states = {state_key(): step_num}

    while True:
        step_num += 1
        step(moons)

        key = state_key()
        last_seen = states.get(key)
        if last_seen is not None:
            return step_num - last_seen, last_seen

        states[key] = step_num

def part2(s):
    moons = list(parse_moons(s))

    answer = lib.math.chinese_remainder([get_cycle_congruence(moons, 0),
                                         get_cycle_congruence(moons, 1),
                                         get_cycle_congruence(moons, 2)],
                                        1)

    lib.aoc.give_answer(2019, 12, 2, answer)

INPUT = lib.aoc.get_input(2019, 12)
part1(INPUT)
part2(INPUT)
