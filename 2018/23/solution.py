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

    lib.aoc.give_answer(2018, 23, 1, answer)

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
    tot_weight = sum(1/(r**3) for r,_ in bots)
    gx = round(sum(x/(r**3) for r, (x, y, z) in bots) / tot_weight)
    gy = round(sum(y/(r**3) for r, (x, y, z) in bots) / tot_weight)
    gz = round(sum(z/(r**3) for r, (x, y, z) in bots) / tot_weight)

    IN_RANGE = bots_in_range(bots, gx, gy, gz)
    DIST = abs(gx) + abs(gy) + abs(gz)

    while True:
        best_count = (IN_RANGE, (gx, gy, gz))
        best_dist = (DIST, (gx, gy, gz))

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if dx == dy == dz == 0:
                        continue

                    factor = 1
                    last_count = IN_RANGE
                    last_dist = DIST
                    while True:
                        nx = gx + dx * factor
                        ny = gy + dy * factor
                        nz = gz + dz * factor

                        count = bots_in_range(bots, nx, ny, nz)
                        if count < last_count:
                            break
                        if count > last_count:
                            last_count = count
                            if best_count[0] < count:
                                best_count = (count, (nx, ny, nz))

                        dist = abs(nx) + abs(ny) + abs(nz)
                        if dist < last_dist:
                            last_dist = dist
                            if best_dist[0] > dist:
                                best_dist = (dist, (nx, ny, nz))

                        factor *= 2

        if best_count[0] > IN_RANGE:
            IN_RANGE, (gx, gy, gz) = best_count
            DIST = abs(gx) + abs(gy) + abs(gz)
            continue

        if best_dist[0] < DIST:
            DIST, (gx, gy, gz) = best_dist
            continue

        # We made no improvement, this should be the answer
        break

    answer = DIST

    lib.aoc.give_answer(2018, 23, 2, answer)

INPUT = lib.aoc.get_input(2018, 23)
part1(INPUT)
part2(INPUT)
