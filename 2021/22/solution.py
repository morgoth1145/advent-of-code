import lib.aoc

def cuboid_intersect(base, other):
    return tuple(range(max(b.start, o.start),
                       min(b.stop, o.stop))
                 for b, o in zip(base, other))

def cuboid_volume(cuboid):
    x, y, z = tuple(map(len, cuboid))
    return x * y * z

def unique_cuboid_volume(cuboid, rest):
    conflicts = []

    for act, other in rest:
        intersection = cuboid_intersect(cuboid, other)
        if cuboid_volume(intersection) == 0:
            continue

        conflicts.append((act, intersection))

    volume = cuboid_volume(cuboid)
    volume -= sum(unique_cuboid_volume(conflict, conflicts[idx+1:])
                  for idx, (_, conflict) in enumerate(conflicts))

    return volume

def parse_range(s):
    c0, c1 = s[2:].split('..')
    return range(int(c0), int(c1)+1)

def solve(s, area_of_interest=None):
    steps = []
    for line in s.splitlines():
        act, cuboid = line.split()
        cuboid = tuple(map(parse_range, cuboid.split(',')))
        if area_of_interest is not None:
            cuboid = cuboid_intersect(cuboid, area_of_interest)
        steps.append((act, cuboid))

    return sum(unique_cuboid_volume(cuboid, steps[idx+1:])
               for idx, (act, cuboid) in enumerate(steps)
               if act == 'on')

def part1(s):
    answer = solve(s, (range(-50, 51), range(-50, 51), range(-50, 51)))

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 22)
part1(INPUT)
part2(INPUT)
