import lib.aoc

def tri(n):
    return n * (n+1) // 2

def x_vel_cands(xrange):
    def range_checker(min_steps, max_steps):
        def impl(steps):
            if steps < min_steps:
                return False
            if max_steps is not None and steps > max_steps:
                return False
            return True
        return impl

    for base_xv in range(xrange[-1]+1):
        if tri(base_xv) < xrange[0]:
            continue

        x, xv = 0, base_xv
        min_steps, max_steps = None, None

        for step in range(xv):
            x, xv = x+xv, xv-1

            if x in xrange and min_steps is None:
                min_steps = step+1
            elif x > xrange[-1]:
                max_steps = step
                break

        if min_steps is not None:
            yield base_xv, range_checker(min_steps, max_steps)

def y_vel_cands(yrange):
    for base_yv in range(yrange[0], abs(yrange[0])):
        good_steps = []

        y, yv, step = 0, base_yv, 0

        while y > yrange[0]:
            y, yv, step = y+yv, yv-1, step+1

            if y in yrange:
                good_steps.append(step)

        if good_steps:
            yield base_yv, good_steps

def solutions(s):
    _, _, x, y = s.split()
    x0, x1 = x[2:-1].split('..')
    y0, y1 = y[2:].split('..')
    xrange = range(int(x0), int(x1)+1)
    yrange = range(int(y0), int(y1)+1)

    x_cands = list(x_vel_cands(xrange))
    y_cands = list(y_vel_cands(yrange))

    for xv, x_step_check in x_cands:
        for yv, y_steps in y_cands:
            if any(map(x_step_check, y_steps)):
                yield xv, yv

def part1(s):
    answer = max(tri(yv)
                 for xv, yv in solutions(s))

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = len(set(solutions(s)))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 17)
part1(INPUT)
part2(INPUT)
