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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 12)
part1(INPUT)
part2(INPUT)
