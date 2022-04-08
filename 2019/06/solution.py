import lib.aoc

def parse_orbits(s):
    orbits = {}

    for line in s.splitlines():
        a, b = line.split(')')
        assert(b not in orbits)
        orbits[b] = a

    return orbits

def part1(s):
    orbits = parse_orbits(s)

    def orbit_count(obj):
        orbiting = orbits.get(obj)
        if orbiting is None:
            return 0

        return 1 + orbit_count(orbiting)

    answer = sum(map(orbit_count, orbits))

    lib.aoc.give_answer(2019, 6, 1, answer)

def get_orbit_list(orbits, obj):
    orbiting = orbits.get(obj)
    if orbiting is None:
        return []

    return [orbiting] + get_orbit_list(orbits, orbiting)

def part2(s):
    orbits = parse_orbits(s)

    san_orbits = get_orbit_list(orbits, 'SAN')
    you_orbits = get_orbit_list(orbits, 'YOU')

    for idx, obj in enumerate(you_orbits):
        if obj in san_orbits:
            # Each step in the orbit lists represents a single jump
            answer = idx + san_orbits.index(obj)
            break

    lib.aoc.give_answer(2019, 6, 2, answer)

INPUT = lib.aoc.get_input(2019, 6)
part1(INPUT)
part2(INPUT)
