import lib.aoc

class Sensor:
    def __init__(self, line):
        parts = line.split()
        self.position = tuple(map(int, (parts[2][2:-1], parts[3][2:-1])))
        self.beacon = tuple(map(int, (parts[8][2:-1], parts[9][2:])))
        self.scan_dist = sum(abs(p-b)
                             for p, b in zip(self.position, self.beacon))

    def in_range(self, x, y):
        dist = sum(abs(p-c) for p, c in zip(self.position, (x, y)))
        return dist <= self.scan_dist

    def potential_candidates(self, other):
        # TODO
        return []

def part1(s):
    sensors = list(map(Sensor, s.splitlines()))

    TARGET_Y = 2000000

    beacons_in_row = len(set(s.beacon[0] for s in sensors
                             if s.beacon[1] == TARGET_Y))

    visible_ranges = []
    for s in sensors:
        half_width = s.scan_dist - abs(s.position[1] - TARGET_Y)
        if half_width < 0:
            continue

        visible_ranges.append((s.position[0] - half_width,
                               s.position[0] + half_width))

    visible_ranges.sort()

    compact = []
    low_x, high_x = visible_ranges[0]
    for n_low_x, n_high_x in visible_ranges[1:]:
        if n_low_x-1 <= high_x:
            high_x = max(high_x, n_high_x)
        else:
            compact.append((low_x, high_x))
            low_x, high_x = n_low_x, n_high_x
    compact.append((low_x, high_x))

    answer = sum(high-low+1 for low, high in compact) - beacons_in_row

    lib.aoc.give_answer(2022, 15, 1, answer)

# TODO: It turns out that we can get all pairs of sensors (there are only a few
# dozen!) and find the couple candidate tiles that are 1 tile outside both
# of their ranges. Unless the distress beacon is in a corner (easy to check)
# then the distress beacon *must* be in one of those candidate tiles.
# That will run *way* faster, though it's also more to think through than I'm
# up for at this point.
def part2(s):
    sensors = list(map(Sensor, s.splitlines()))

    MIN_COORD = 0
    MAX_COORD = 4000000

    # Make sure to check the 4 corners
    candidates = {(x, y)
                  for x in (MIN_COORD, MAX_COORD)
                  for y in (MIN_COORD, MAX_COORD)}

    # Add candidate positions for all pairs of scanners
    for idx, s0 in enumerate(sensors):
        for s1 in sensors[idx+1:]:
            candidates.update(s0.potential_candidates(s1))

    for x, y in candidates:
        if (MIN_COORD <= x <= MAX_COORD and MIN_COORD <= y <= MAX_COORD
            and not any(s.in_range(x, y) for s in sensors)):
            print(f'Valid solution at {x},{y}')
            print(f'Answer would be {x * 4000000 + y}')

    for y in range(MIN_COORD, MAX_COORD+1):
        ranges = []
        for s in sensors:
            half_width = s.scan_dist - abs(s.position[1] - y)
            if half_width < 0:
                continue

            ranges.append((s.position[0] - half_width,
                           s.position[0] + half_width))

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
            answer = x * 4000000 + y
            break

    lib.aoc.give_answer(2022, 15, 2, answer)

INPUT = lib.aoc.get_input(2022, 15)
part1(INPUT)
part2(INPUT)
