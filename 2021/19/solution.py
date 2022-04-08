import collections

import lib.aoc
from lib.graphics import *

ROTATIONS = []
for x in [X_AXIS, -X_AXIS, Y_AXIS, -Y_AXIS, Z_AXIS, -Z_AXIS]:
    for y in [X_AXIS, -X_AXIS, Y_AXIS, -Y_AXIS, Z_AXIS, -Z_AXIS]:
        if x.dot(y) != 0:
            continue
        ROTATIONS.append(Mat3D(x, y))

def manhattan_distance(a, b):
    return sum(map(abs, a - b))

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.position = Point3D(0, 0, 0)

        self._beacon_dist_counts = collections.Counter()

        for i, a in enumerate(self.beacons):
            for j, b in enumerate(self.beacons[i+1:]):
                dist = manhattan_distance(a, b)
                # Count for both a->b and b->a
                self._beacon_dist_counts[dist] += 2

    def align(self, base):
        # Counter intersection: Takes the minimum
        shared_dists = self._beacon_dist_counts & base._beacon_dist_counts
        matches = sum(shared_dists.values())

        # If the two beacons line up then there must be at least 12 beacons
        # that will align in some orientation. For each of those 12 beacons,
        # the manhattan distance to the other 11 beacons will match. If we
        # do not see that many matches then these two scanners can't align!
        if sum(shared_dists.values()) < 12*11:
            return None

        for rot in ROTATIONS:
            cand_beacons = [rot * p for p in self.beacons]

            offset_matches = collections.Counter([base_c - test_c
                                                  for base_c in base.beacons
                                                  for test_c in cand_beacons])
            offset, count = offset_matches.most_common(1)[0]
            if count < 12:
                # No match :(
                continue

            # Apply the alignment
            self.beacons = [p + offset for p in cand_beacons]
            self.position = offset
            return True

        return False

def solve(s):
    to_align = [Scanner([Point3D(*tuple(map(int, line.split(','))))
                         for line in group.splitlines()[1:]])
                for group in s.split('\n\n')]

    scanners = [to_align.pop(0)]

    for base in scanners:
        failed = []

        for s in to_align:
            if s.align(base):
                scanners.append(s)
            else:
                failed.append(s)

        to_align = failed

    assert(len(to_align) == 0)

    beacons = set()
    for s in scanners:
        beacons.update(s.beacons)

    return beacons, scanners

def part1(s):
    beacons, scanners = solve(s)
    answer = len(beacons)

    lib.aoc.give_answer(2021, 19, 1, answer)

def part2(s):
    beacons, scanners = solve(s)
    answer = max(manhattan_distance(s0.position, s1.position)
                 for s0 in scanners
                 for s1 in scanners)

    lib.aoc.give_answer(2021, 19, 2, answer)

INPUT = lib.aoc.get_input(2021, 19)
part1(INPUT)
part2(INPUT)
