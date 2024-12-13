import functools

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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 13)
part1(INPUT)
part2(INPUT)
