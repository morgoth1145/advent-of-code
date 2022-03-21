import math

import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    answer = 0

    for (x, y), c in grid.items():
        if c == '.':
            continue
        angles = set()
        for (ox, oy), c in grid.items():
            if c == '.':
                continue
            if x == ox and y == oy:
                continue

            dx, dy = x-ox, y-oy
            if dx == 0:
                if dy > 0:
                    angles.add((0, 1))
                else:
                    angles.add((0, -1))
            elif dy == 0:
                if dx > 0:
                    angles.add((1, 0))
                else:
                    angles.add((-1, 0))
            else:
                # Simplify the angle
                denom = math.gcd(abs(dx), abs(dy))
                dx /= denom
                dy /= denom
                angles.add((dx, dy))

        # len(angles) tells us how many angles survived, so how many asteroids
        # we can see
        answer = max(answer, len(angles))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 10)
part1(INPUT)
part2(INPUT)
