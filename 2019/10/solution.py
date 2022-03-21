import collections
import math

import lib.aoc
import lib.grid

def compute_minimum_angle(dx, dy):
    if dx == 0:
        if dy > 0:
            return 0, 1
        else:
            return 0, -1
    if dy == 0:
        if dx > 0:
            return 1, 0
        else:
            return -1, 0
    else:
        # Simplify the angle
        denom = math.gcd(abs(dx), abs(dy))
        return dx // denom, dy // denom

# Constructs a map of angle to which asteroids are visible at that angle
def determine_asteroid_visibility(grid, x, y):
    asteroids = collections.defaultdict(set)

    for (ox, oy), c in grid.items():
        if c == '.':
            continue
        if x == ox and y == oy:
            continue

        asteroids[compute_minimum_angle(ox-x, oy-y)].add((ox, oy))

    return asteroids

def get_best_asteroid(grid):
    best = (0, None)

    for (x, y), c in grid.items():
        if c == '.':
            continue

        asteroids = determine_asteroid_visibility(grid, x, y)

        # len(angles) tells us how many angles survived, so how many asteroids
        # we can see
        best = max(best, (len(asteroids), (x, y)))

    return best[1]

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    x, y = get_best_asteroid(grid)

    answer = len(determine_asteroid_visibility(grid, x, y))

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    x, y = get_best_asteroid(grid)

    asteroids = determine_asteroid_visibility(grid, x, y)

    right_side_angles = []
    left_side_angles = []

    for dx, dy in asteroids:
        if dx > 0:
            right_side_angles.append((dx, dy))
        elif dx < 0:
            left_side_angles.append((dx, dy))

    # Order angles in the right quadrant from top to bottom
    right_side_angles.sort(key=lambda a: a[1]/a[0],
                           reverse=True)

    # Order angles in the right quadrant from bottom to top
    left_side_angles.sort(key=lambda a: a[1]/a[0])

    angle_order = []
    if (0, 1) in asteroids:
        angle_order.append((0, 1))
    angle_order += right_side_angles
    if (0, -1) in asteroids:
        angle_order.append((0, -1))
    angle_order += left_side_angles

    destruction_order = []

    while len(destruction_order) < 200:
        for a in angle_order:
            if len(asteroids[a]) == 0:
                continue

            target = min(asteroids[a], key=lambda o: abs(o[0]-x) + abs(o[1]-y))

            asteroids[a].remove(target)
            destruction_order.append(target)

    x, y = destruction_order[199]

    answer = x * 100 + y

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 10)
part1(INPUT)
part2(INPUT)
