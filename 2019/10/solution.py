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
    asteroids = collections.defaultdict(list)

    for (ox, oy), c in grid.items():
        if c == '.':
            continue
        if x == ox and y == oy:
            continue

        asteroids[compute_minimum_angle(ox-x, oy-y)].append((ox, oy))

    for asteroid_list in asteroids.values():
        asteroid_list.sort(key=lambda a: abs(a[0]-x) + abs(a[1]-y))

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

    angle_order = sorted(asteroids,
                         key=lambda a: math.atan2(a[1], a[0]))

    # Find the first angle that's either pointing up or in the right quadrant
    # Once found, rotate the angle order as needed
    shift_idx = min(i for i in range(len(angle_order))
                    if math.atan2(angle_order[i][1],
                                  angle_order[i][0]) >= math.atan2(-1, 0))
    angle_order = angle_order[shift_idx:] + angle_order[:shift_idx]

    destruction_order = []

    while angle_order:
        new_angle_order = []

        for a in angle_order:
            asteroid_list = asteroids[a]
            destruction_order.append(asteroid_list.pop(0))

            if len(asteroid_list) > 0:
                new_angle_order.append(a)

        angle_order = new_angle_order

    x, y = destruction_order[199]

    answer = x * 100 + y

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 10)
part1(INPUT)
part2(INPUT)
