import collections
import parse

import lib.aoc

def parse_all_ints(s):
    return list(map(lambda r:r[0], parse.findall('{:d}', s)))

def parse_input(s):
    for line in s.splitlines():
        px, py, vx, vy = parse_all_ints(line)
        yield [(px, py), (vx, vy)]

def step_robot(px, py, vx, vy, width, height):
    px += vx
    py += vy

    if px < 0:
        px += width
    if px >= width:
        px -= width

    if py < 0:
        py += height
    if py >= height:
        py -= height

    return px, py

def project(robot, width, height, steps):
    (px, py), (vx, vy) = robot

    for _ in range(steps):
        px, py = step_robot(px, py, vx, vy, width, height)

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
    robots = list(parse_input(s))

    WIDTH = 101
    HEIGHT = 103

    MIDDLE_X = WIDTH//2
    MIDDLE_Y = HEIGHT//2

    def maybe_christmas(px, py):
        x = abs(px - MIDDLE_X)
        return (py+2)//2 > x

    def tree_score():
        return sum(maybe_christmas(px, py)
                   for (px, py), _
                   in robots)

    def print_state():
        has_bot = set(p for p, v in robots)

        for y in range(HEIGHT):
            l = ''
            for x in range(WIDTH):
                if maybe_christmas(x, y):
                    c = 'T' if (x,y) in has_bot else '.'
                else:
                    c = '#' if (x,y) in has_bot else ' '
                l += c
            print(l)

        print('-'*75)
        print('-'*75)
        print('-'*75)

    answer = 0
    best_score = -1

    for i in range(50000):
        s = tree_score()
        if s > best_score:
            print(i)
            print_state()
            answer = i
            best_score = s
        for idx, robot in enumerate(robots):
            (px, py), (vx, vy) = robot
            px, py = step_robot(px, py, vx, vy, WIDTH, HEIGHT)
            robot[0] = (px, py)

    lib.aoc.give_answer(2024, 14, 2, answer)

INPUT = lib.aoc.get_input(2024, 14)
part1(INPUT)
part2(INPUT)
