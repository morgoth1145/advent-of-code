import z3

import lib.aoc

def solve(s, a_cost, b_cost, px_offset=0, py_offset=0, press_limit=None):
    answer = 0

    for group in s.split('\n\n'):
        # Janky parsing!
        group = (group
                 .replace('X', '')
                 .replace('Y', '')
                 .replace('+', '')
                 .replace('=', ''))
        (ax, ay), (bx, by), (px, py) = [list(map(int,
                                                 line.split(': ')[1]
                                                 .split(',')))
                                        for line in group.splitlines()]

        o = z3.Optimize()
        a = z3.Int('a')
        b = z3.Int('b')
        cost = z3.Int('cost')

        o.add([a*ax + b*bx == px+px_offset,
               a*ay + b*by == py+py_offset,
               cost == a*a_cost + b*b_cost])
        if press_limit is not None:
            o.add([a <= press_limit,
                   b <= press_limit])
        o.minimize(cost)
        o.check()

        cost = o.model()[cost]

        if cost is not None:
            answer += cost.as_long()

    return answer

def part1(s):
    answer = solve(s, 3, 1, press_limit=100)

    lib.aoc.give_answer(2024, 13, 1, answer)

def part2(s):
    OFFSET = 10000000000000
    answer = solve(s, 3, 1, px_offset=OFFSET, py_offset=OFFSET)

    lib.aoc.give_answer(2024, 13, 2, answer)

INPUT = lib.aoc.get_input(2024, 13)
part1(INPUT)
part2(INPUT)
