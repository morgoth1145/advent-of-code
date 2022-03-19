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
    bots = list(parse_bots(s))

    # Guess the center as the weighted average of the bots
    # (The weight is the inverse of the radius)
    gx = round(sum(x/r for r, (x, y, z) in bots) / sum(1/r for r,_ in bots))
    gy = round(sum(y/r for r, (x, y, z) in bots) / sum(1/r for r,_ in bots))
    gz = round(sum(z/r for r, (x, y, z) in bots) / sum(1/r for r,_ in bots))

    best_count = 0
    best_dist = 0

    while True:
        improved = False

        dx = -1 if gx > 0 else 1
        dy = -1 if gy > 0 else 1
        dz = -1 if gz > 0 else 1

        for factor in (100000, 10000, 1000, 100, 10, 1):
            for fx in (-4, -2, -1, 0, 1, 2, 4):
                for fy in (-4, -2, -1, 0, 1, 2, 4):
                    for fz in (-4, -2, -1, 0, 1, 2, 4):
                        if fx == fy == fz:
                            continue
                        while True:
                            nx = gx + dx * fx * factor
                            ny = gy + dy * fy * factor
                            nz = gz + dz * fz * factor
                            count = bots_in_range(bots, nx, ny, nz)
                            dist = abs(nx) + abs(ny) + abs(nz)
                            if count < best_count:
                                break
                            if count == best_count and dist > best_dist:
                                break
                            improved = True
                            best_count = count
                            best_dist = dist
                            gx, gy, gz = nx, ny, nz

        if not improved:
            break

    answer = abs(gx) + abs(gy) + abs(gz)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 23)
part1(INPUT)
part2(INPUT)
