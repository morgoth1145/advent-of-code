import parse

import lib.aoc

def parse_ranges(s):
    x0, x1, y0, y1 = parse.parse('target area: x={:d}..{:d}, y={:d}..{:d}', s)
    xrange = range(int(x0), int(x1)+1)
    yrange = range(int(y0), int(y1)+1)
    return xrange, yrange

def tri(n):
    return n * (n+1) // 2

def part1(s):
    _, yrange = parse_ranges(s)

    # Any negative initial y velocity does not reach above 0
    # Furthermore, we know that any positive initial y velocity will, after
    # some number of steps, get back to 0 with velocity -initial_y_velocity - 1.
    # (It follows a parabola!)
    # The maximum initial y velocity to stay inside the target is thus
    # abs(y0)-1, assuming that y0 is negative (which it is for this problem).
    max_yv = abs(yrange[0])-1
    answer = tri(max_yv)

    print(f'The answer to part one is {answer}')

def sum_range(first, last):
    n = abs(first - last) + 1
    return n * (first + last) // 2

def x_vel_solutions(xrange):
    solutions = []

    min_steps = 1
    max_steps = 0

    for base_xv in range(xrange[-1], 0, -1):
        if tri(base_xv) < xrange[0]:
            break

        # min_steps is guaranteed to not pass xrange (per the above check)
        x = sum_range(base_xv, base_xv-min_steps+1)
        xv = base_xv - min_steps

        while x < xrange[0]:
            x, xv = x+xv, xv-1
            min_steps += 1

        if x not in xrange:
            continue

        if max_steps is None:
            # It's unbounded!
            solutions.append((base_xv, min_steps, max_steps))
            continue

        step = min_steps

        if max_steps > step:
            jump_steps = max_steps - step
            step = max_steps
            if xv <= jump_steps:
                x += tri(xv)
                xv = 0
            else:
                x += sum_range(xv, xv - jump_steps + 1)
                xv -= jump_steps
        else:
            max_steps = step

        while xv != 0 and x <= xrange[-1]:
            max_steps = step
            x, xv, step = x+xv, xv-1, step+1

        if xv == 0 and x in xrange:
            # Signal that it's unbounded
            max_steps = None

        solutions.append((base_xv, min_steps, max_steps))

    return solutions

def y_vel_solutions(yrange):
    solutions = []

    min_steps = 1
    max_steps = 0

    for base_yv in range(yrange[0], abs(yrange[0])):
        y = sum_range(base_yv, base_yv-min_steps+1)
        yv = base_yv - min_steps
        step = min_steps

        while y > yrange[-1]:
            y, yv, step = y+yv, yv-1, step+1
            min_steps += 1

        if y < yrange[0]:
            continue

        step = min_steps

        if max_steps > step:
            jump_steps = max_steps - step
            step = max_steps
            y += sum_range(yv, yv - jump_steps + 1)
            yv -= jump_steps
        else:
            max_steps = step

        max_steps = step
        while y >= yrange[0]:
            max_steps = step
            y, yv, step = y+yv, yv-1, step+1

        solutions.append((base_yv, min_steps, max_steps))

    return solutions

def part2(s):
    xrange, yrange = parse_ranges(s)

    # x and y solutions have ranges of steps for which they are valid
    # The minimum and maximum bounds of these ranges are monotonicaly increasing
    x_solutions = x_vel_solutions(xrange)
    y_solutions = y_vel_solutions(yrange)

    # If we keep track of when x solutions enter and exit the range we care
    # about (based on the step count) then we can easily know how many solutions
    # exist for a given y velocity (since it's just the number of matching
    # x solutions).
    x_add_sol_stack = [max_steps
                       for xv, min_steps, max_steps in x_solutions
                       if max_steps is not None]
    x_remove_sol_stack = [min_steps
                          for xv, min_steps, max_steps in x_solutions]

    # All unbounded x solutions start as matching!
    x_match_count = sum(1
                        for xv, min_steps, max_steps in x_solutions
                        if max_steps is None)

    answer = 0

    for yv, min_steps, max_steps in y_solutions[::-1]:
        # Remove expired x solutions which fell out of the range
        while x_remove_sol_stack and x_remove_sol_stack[-1] > max_steps:
            x_remove_sol_stack.pop(-1)
            x_match_count -= 1
        # Add new x solutions which entered the range
        while x_add_sol_stack and x_add_sol_stack[-1] >= min_steps:
            x_add_sol_stack.pop(-1)
            x_match_count += 1

        answer += x_match_count

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 17)
part1(INPUT)
part2(INPUT)
