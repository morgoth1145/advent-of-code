import collections
import parse

import lib.aoc

def parse_all_ints(s):
    return list(map(lambda r:r[0], parse.findall('{:d}', s)))

def parse_input(s):
    for line in s.splitlines():
        px, py, vx, vy = parse_all_ints(line)
        yield (px, py), (vx, vy)

def project(robot, width, height, steps):
    (px, py), (vx, vy) = robot

    px += steps * vx
    py += steps * vy

    while px < 0:
        px += width
    while px >= width:
        px -= width

    while py < 0:
        py += height
    while py >= height:
        py -= height

    return px, py

def part1(s):
    data = parse_input(s)

    WIDTH = 101
    HEIGHT = 103

    MIDDLE_X = WIDTH//2
    MIDDLE_Y = HEIGHT//2

    quadrants = collections.Counter()

    for robot in data:
        px, py = project(robot, 101, 103, 100)

        if px == MIDDLE_X or py == MIDDLE_Y:
            continue

        qx = px > MIDDLE_X
        qy = py > MIDDLE_Y
        quadrants[qx,qy] += 1

    answer = 1

    for v in quadrants.values():
        answer *= v

    lib.aoc.give_answer(2024, 14, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 14)
part1(INPUT)
part2(INPUT)
