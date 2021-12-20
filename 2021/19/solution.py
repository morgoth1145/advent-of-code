import collections

import lib.aoc
from lib.graphics import *

ROTATIONS = []
for x in [X_AXIS, -X_AXIS, Y_AXIS, -Y_AXIS, Z_AXIS, -Z_AXIS]:
    for y in [X_AXIS, -X_AXIS, Y_AXIS, -Y_AXIS, Z_AXIS, -Z_AXIS]:
        if x.dot(y) != 0:
            continue
        ROTATIONS.append(Mat3D(x, y))

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self._alt_orients = None

    def beacon_orientations(self):
        if self._alt_orients is None:
            self._alt_orients = [[rot * p for p in self.beacons]
                                 for rot in ROTATIONS]
        return self._alt_orients

def parse_scans(s):
    groups = s.split('\n\n')
    for idx, scanner in enumerate(groups):
        lines = scanner.splitlines()
        beacons = []
        for line in lines[1:]:
            x, y, z = tuple(map(int, line.split(',')))
            beacons.append(Point3D(x, y, z))
        yield Scanner(beacons)

def find_scanner_matches(known, scanners):
    failed = []

    for s in scanners:
        matched = False
        for beacon_orient in s.beacon_orientations():
            offset_matches = collections.Counter([base_c - test_c
                                                  for base_c in known.beacons
                                                  for test_c in beacon_orient])
            offset, count = offset_matches.most_common(1)[0]
            if count < 12:
                # No match :(
                continue

            yield Scanner([p + offset for p in beacon_orient]), offset
            matched = True
            break
        if not matched:
            failed.append(s)

    del scanners[:]
    scanners.extend(failed)

def solve(s):
    unmatched_scanners = list(parse_scans(s))

    to_handle = [unmatched_scanners[0]]
    beacons = set(unmatched_scanners[0].beacons)
    del unmatched_scanners[0]
    scanners = [Point3D(0, 0, 0)]

    while to_handle:
        base = to_handle.pop(-1)
        for match, offset in find_scanner_matches(base, unmatched_scanners):
            beacons.update(match.beacons)
            scanners.append(offset)
            to_handle.append(match)

    assert(len(unmatched_scanners) == 0)

    return beacons, scanners

def part1(s):
    beacons, scanners = solve(s)
    answer = len(beacons)

    print(f'The answer to part one is {answer}')

def part2(s):
    beacons, scanners = solve(s)
    # Maximum Manhattan distance between scanners
    answer = max(sum(map(abs, (s0 - s1)))
                 for s0 in scanners
                 for s1 in scanners)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 19)
part1(INPUT)
part2(INPUT)
