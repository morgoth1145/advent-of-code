import collections
import math

import lib.aoc
import lib.math

class Robots:
    def __init__(self, s, width, height):
        self.robots = []
        for line in s.splitlines():
            p, v = line.split()
            p = tuple(map(int, p[2:].split(',')))
            v = tuple(map(int, v[2:].split(',')))
            self.robots.append([p, v])

        self.width = width
        self.height = height

    def step(self):
        for robot in self.robots:
            (px, py), (vx, vy) = robot
            px = (px + vx) % self.width
            py = (py + vy) % self.height
            robot[0] = (px, py)

    @property
    def safety_factor(self):
        quadrants = {(qx, qy): 0
                     for qx in (0, 1)
                     for qy in (0, 1)}

        middle_x = self.width//2
        middle_y = self.height//2

        for (px, py), _ in self.robots:
            if px == middle_x or py == middle_y:
                continue

            qx = px > middle_x
            qy = py > middle_y
            quadrants[qx,qy] += 1

        safety = 1
        for v in quadrants.values():
            safety *= v

        return safety

    @property
    def robot_state_key(self):
        return [p for p, v in self.robots]

def part1(s):
    robots = Robots(s, 101, 103)

    for _ in range(100):
        robots.step()

    answer = robots.safety_factor

    lib.aoc.give_answer(2024, 14, 1, answer)

def part2(s):
    WIDTH = 101
    HEIGHT = 103

    assert(math.gcd(WIDTH, HEIGHT) == 1)

    robots = Robots(s, WIDTH, HEIGHT)

    best_x = None
    best_y = None

    for iter_n in range(max(WIDTH, HEIGHT)):
        c_x = collections.Counter(px for px, py in robots.robot_state_key)
        key_x = sorted(c_x.values(), reverse=True)
        if best_x is None or key_x > best_x[0]:
            best_x = (key_x, iter_n)

        c_y = collections.Counter(py for px, py in robots.robot_state_key)
        key_y = sorted(c_y.values(), reverse=True)
        if best_y is None or key_y > best_y[0]:
            best_y = (key_y, iter_n)

        robots.step()

    x_offset = best_x[1]
    y_offset = best_y[1]

    # Assume that the tree shows up with the maximum "clustering" in each dimension
    # This can be computed significantly faster than checking 10k states!
    answer = lib.math.chinese_remainder([(WIDTH, x_offset),
                                         (HEIGHT, y_offset)])

    lib.aoc.give_answer(2024, 14, 2, answer)

INPUT = lib.aoc.get_input(2024, 14)
part1(INPUT)
part2(INPUT)
