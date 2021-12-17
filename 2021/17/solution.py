import lib.aoc

def parse(s):
    _, _, x, y = s.split()
    x = x[2:-1]
    y = y[2:]
    x0, x1 = x.split('..')
    y0, y1 = y.split('..')
    return int(x0), int(x1), int(y0), int(y1)

def tri(n):
    return n * (n+1) // 2

def x_vel_cands(xrange):
    x = 0
    while tri(x) < xrange[0]:
        x += 1
    yield x
    x += 1
    while x < xrange[-1]:
        if any(tri(x) - tri(lowx)
               for lowx in range(x)):
            yield x
        x += 1

def cand_steps_x(xv, xrange):
    x = 0
    steps = 0
    min_steps = None
    max_steps = None
    while True:
        x += xv
        xv = max(xv-1, 0)
        steps += 1
        if x in xrange:
            if min_steps is None:
                min_steps = steps
        if x > xrange[-1]:
            return min_steps, steps-1
        if xv == 0:
            # Probably no :(
            return min_steps, None

def y_helper(yv, yrange, max_steps):
    y = 0
    best_y = 0
    last_y = 0
    for _ in range(max_steps):
        last_y = y
        y += yv
        yv -= 1
        best_y = max(best_y, y)
        if y in yrange:
            return best_y
        if last_y > yrange[-1] and y < yrange[0]:
            return False
    if y > yrange[-1]:
        return False
    return None

def search_y(yrange, xv, xrange):
    min_steps, max_steps = cand_steps_x(xv, xrange)
    if min_steps is None:
        return 0

    if max_steps is None:
        max_steps = 2*abs(yrange[0])

    cand_steps = range(min_steps, max_steps+1)

    yv = 1
    best_y = 0
    for steps in cand_steps:
        yv = 0
        while yv <= abs(yrange[0]):
            yv += 1
            y = y_helper(yv, yrange, steps)
            if y is None:
                continue
            best_y = max(y, best_y)

    return best_y

def y_vel_cands(yrange, max_steps):
    yv = 1
    while True:
        y = y_helper(yv, max_steps)
        if y > yrange[-1]:
            # Didn't even enter
            return
        yield y

def part1(s):
    x0, x1, y0, y1 = parse(s)
    xrange = range(x0, x1+1)
    yrange = range(y0, y1+1)

    best_y = 0

    for xv in x_vel_cands(xrange):
        y = search_y(yrange, xv, xrange)
        best_y = max(y, best_y)

    answer = best_y

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 17)
part1(INPUT)
part2(INPUT)
