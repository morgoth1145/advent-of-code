import functools
import z3

import lib.aoc

def parse_input(s):
    def parse_xy(st):
        x, y = st.split(', ')
        assert(x[0] == 'X' and y[0] == 'Y')
        return int(x[1:]), int(y[1:])
    for group in s.split('\n\n'):
        group = group.replace('+', '').replace('=', '')
        lines = group.splitlines()
        a = lines[0].split(': ')[1]
        b = lines[1].split(': ')[1]
        prize = lines[2].split(': ')[1]

        yield parse_xy(a), parse_xy(b), parse_xy(prize)

def optimize_cost(a_delta, a_cost, b_delta, b_cost, prize):
    @functools.cache
    def impl(x, y, a_left, b_left):
        if (x, y) == prize:
            return 0
        if x > prize[0] or y > prize[1]:
            return None

        cost = None

        if a_left > 0:
            took_a_cost = impl(x+a_delta[0], y+a_delta[1], a_left-1, b_left)
            if took_a_cost is not None:
                cost = took_a_cost + a_cost

        if b_left > 0:
            took_b_cost = impl(x+b_delta[0], y+b_delta[1], a_left, b_left-1)
            if took_b_cost is not None:
                temp_cost = took_b_cost + b_cost
                if cost is None or temp_cost < cost:
                    cost = temp_cost

        return cost

    return impl(0, 0, 100, 100)

def part1(s):
    data = list(parse_input(s))

    answer = 0

    for a, b, prize in data:
        cost = optimize_cost(a, 3, b, 1, prize)
        if cost is not None:
            answer += cost

    lib.aoc.give_answer(2024, 13, 1, answer)

def optimize_cost2(a_delta, a_cost, b_delta, b_cost, prize, press_limit=None):
    ax, ay = a_delta
    bx, by = b_delta
    px, py = prize

    a_times = z3.Int('a_times')
    b_times = z3.Int('b_times')
    cost = z3.Int('cost')

    o = z3.Optimize()
    o.add(a_times*ax + b_times*bx == px)
    o.add(a_times*ay + b_times*by == py)
    if press_limit is not None:
        o.add(a_times <= press_limit)
        o.add(b_times <= press_limit)

    o.add(cost == a_times*a_cost + b_times*b_cost)
    o.minimize(cost)
    o.check()

    cost = o.model()[cost]

    return cost.as_long() if cost is not None else None

def part2(s):
    data = list(parse_input(s))

    answer = 0

    for a, b, prize in data:
        px, py = prize
        prize = (10000000000000+px, 10000000000000+py)
        cost = optimize_cost2(a, 3, b, 1, prize)
        if cost is not None:
            answer += cost

    lib.aoc.give_answer(2024, 13, 2, answer)

INPUT = lib.aoc.get_input(2024, 13)
part1(INPUT)
part2(INPUT)
