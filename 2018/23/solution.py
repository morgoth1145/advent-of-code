import lib.aoc

def parse_bots(s):
    bots = []

    for line in s.splitlines():
        line = line.replace('pos=<', '').replace('>', '').replace('r=', '')
        x, y, z, r = tuple(map(int, line.split(',')))
        bots.append((r, (x, y, z)))

    return bots

def part1(s):
    bots = sorted(parse_bots(s))

    r, (cx, cy, cz) = bots[-1]

    answer = 0

    for _, (x, y, z) in bots:
        if abs(x-cx) + abs(y-cy) + abs(z-cz) <= r:
            answer += 1

    print(f'The answer to part one is {answer}')

def bots_in_range(bots, gx, gy, gz):
    count = 0

    for r, (x, y, z) in bots:
        if abs(x-gx) + abs(y-gy) + abs(z-gz) <= r:
            count += 1

    return count

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 23)
part1(INPUT)
part2(INPUT)
