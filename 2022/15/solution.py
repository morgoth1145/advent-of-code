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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 15)
part1(INPUT)
part2(INPUT)
