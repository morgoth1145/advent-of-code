import parse

import lib.aoc

def parse_all_ints(s):
    return list(map(lambda r:r[0], parse.findall('{:d}', s)))

def parse_input(s):
    for line in s.splitlines():
        sens_x, sens_y, beacon_x, beacon_y = parse_all_ints(line)
        yield (sens_x, sens_y), (beacon_x, beacon_y)

def part1(s):
    data = list(parse_input(s))

    TARGET_Y = 2000000

    beacons = set((beac_x, beac_y)
                  for (sens_x, sens_y), (beac_x, beac_y) in data)

    no_beacons = set()

    for (sens_x, sens_y), (beac_x, beac_y) in data:
        min_manhattan = abs(sens_x-beac_x) + abs(sens_y-beac_y)

        for dx in (1, -1):
            dist = abs(sens_y - TARGET_Y)
            x = sens_x
            while dist <= min_manhattan:
                no_beacons.add((x, TARGET_Y))
                x += dx
                dist += 1

    answer = len(no_beacons - beacons)

    lib.aoc.give_answer(2022, 15, 1, answer)

# Probably super inefficient but I don't care! It worked!
def part2_search(s):
    data = list(parse_input(s))

    MIN_COORD = 0
    MAX_COORD = 4000000

    for y in range(MIN_COORD, MAX_COORD+1):
        ranges = []
        for (sens_x, sens_y), (beac_x, beac_y) in data:
            min_manhattan = abs(sens_x-beac_x) + abs(sens_y-beac_y)

            dist = abs(sens_y - y)
            mult = min_manhattan - dist
            if mult < 0:
                continue

            ranges.append((sens_x - mult, sens_x + mult))

        ranges.sort()

        compact = []
        low_x, high_x = ranges[0]
        for n_low_x, n_high_x in ranges[1:]:
            if n_low_x-1 <= high_x:
                high_x = max(high_x, n_high_x)
            else:
                compact.append((low_x, high_x))
                low_x, high_x = n_low_x, n_high_x
        compact.append((low_x, high_x))

        if len(compact) != 1:
            assert(len(compact) == 2)
            (a, b), (c, d) = compact
            assert(b+2 == c)
            x = b+1
            return x * 4000000 + y

def part2(s):
    answer = part2_search(s)

    lib.aoc.give_answer(2022, 15, 2, answer)

INPUT = lib.aoc.get_input(2022, 15)
part1(INPUT)
part2(INPUT)
