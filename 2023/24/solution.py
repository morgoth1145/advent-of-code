import sympy

import lib.aoc
from lib.graphics import *

def parse_input(s):
    for line in s.splitlines():
        p, v = line.split(' @ ')
        p = Point3D(*tuple(map(int, p.split(', '))))
        v = Vec3D(*tuple(map(int, v.split(', '))))
        yield p, v

def part1(s):
    data = list(parse_input(s))

    MIN = 200000000000000
    MAX = 400000000000000

    answer = 0

    for idx, (p1, v1) in enumerate(data):
        for p2, v2 in data[idx+1:]:
            a = v1.y / v1.x

            denom = a * v2.x - v2.y
            if denom == 0:
                continue

            t2 = (p2.y - p1.y + a * p1.x - a * p2.x) / denom
            if t2 < 0:
                continue

            t1 = (p2.x + v2.x * t2 - p1.x) / v1.x
            if t1 < 0:
                continue

            the_p = p1 + v1 * t1

            if MIN <= the_p.x <= MAX:
                if MIN <= the_p.y <= MAX:
                    answer += 1

    lib.aoc.give_answer(2023, 24, 1, answer)

def part2(s):
    data = list(parse_input(s))

    x = sympy.var('x')
    y = sympy.var('y')
    z = sympy.var('z')

    xv = sympy.var('xv')
    yv = sympy.var('yv')
    zv = sympy.var('zv')

    equations = []

    for idx, (p, v) in enumerate(data[:3]):
        t = sympy.var(f't{idx}')

        equations.append(sympy.Eq(x + t * xv, p.x + v.x * t))
        equations.append(sympy.Eq(y + t * yv, p.y + v.y * t))
        equations.append(sympy.Eq(z + t * zv, p.z + v.z * t))

    d = sympy.solve(equations)[0]

    answer = sum(d[v] for v in (x, y, z))

    lib.aoc.give_answer(2023, 24, 2, answer)

INPUT = lib.aoc.get_input(2023, 24)
part1(INPUT)
part2(INPUT)
