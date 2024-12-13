import lib.aoc

def solve(s, a_cost, b_cost, px_offset=0, py_offset=0):
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
        px, py = px+px_offset, py+py_offset

        # a*ax + b*bx = px
        # a*ay + b*by = py
        
        # a = (px - b*bx) / ax
        # ((px - b*bx) / ax) * ay + b*by = py
        # (px - b*bx) * ay + b*ax*by = py*ax
        # px*ay - b*bx*ay + b*ax*by = py*ax
        # b*ax*by - b*bx*ay = py*ax - px*ay
        # b * (ax*by - bx*ay) = py*ax - px*ay
        # b = (py*ax - px*ay) / (ax*by - bx*ay)

        b, brem = divmod(py*ax - px*ay, ax*by - bx*ay)
        if brem != 0 or b < 0:
            continue # Not a valid solution

        a, arem = divmod(px - b*bx, ax)
        if arem != 0 or a < 0:
            continue # Not a valid solution

        answer += a*a_cost + b*b_cost

    return answer

def part1(s):
    answer = solve(s, 3, 1)

    lib.aoc.give_answer(2024, 13, 1, answer)

def part2(s):
    OFFSET = 10000000000000
    answer = solve(s, 3, 1, px_offset=OFFSET, py_offset=OFFSET)

    lib.aoc.give_answer(2024, 13, 2, answer)

INPUT = lib.aoc.get_input(2024, 13)
part1(INPUT)
part2(INPUT)
