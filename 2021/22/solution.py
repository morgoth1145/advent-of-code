import lib.aoc

def clip_range(base, clip):
    if base.stop <= clip.start or base.start >= clip.stop:
        return range(0)
    return range(max(base.start, clip.start), min(base.stop, clip.stop))

def count_uninterrupted(step, rest):
    _, xr, yr, zr = step

    conflicts = []

    for step in rest:
        state, xr2, yr2, zr2 = step

        xr2 = clip_range(xr2, xr)
        yr2 = clip_range(yr2, yr)
        zr2 = clip_range(zr2, zr)

        if len(xr2) == 0 or len(yr2) == 0 or len(zr2) == 0:
            continue

        conflicts.append((state, xr2, yr2, zr2))

    total = len(xr) * len(yr) * len(zr)
    for idx, step in enumerate(conflicts):
        total -= count_uninterrupted(step, conflicts[idx+1:])

    return total

def parse_range(s, window):
    c0, c1 = s[2:].split('..')
    r = range(int(c0), int(c1)+1)
    if window is not None:
        r = clip_range(r, window)
    return r

def solve(s, xwindow=None, ywindow=None, zwindow=None):
    steps = []
    for line in s.splitlines():
        state, rest = line.split()
        x, y, z = rest.split(',')
        steps.append((state,
                      parse_range(x, xwindow),
                      parse_range(y, ywindow),
                      parse_range(z, zwindow)))

    total = 0

    for idx, step in enumerate(steps):
        if step[0] == 'off':
            continue
        total += count_uninterrupted(step, steps[idx+1:])

    return total

def part1(s):
    answer = solve(s, range(-50, 51), range(-50, 51), range(-50, 51))

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 22)
part1(INPUT)
part2(INPUT)
