import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        state, rest = line.split()
        x, y, z = rest.split(',')
        x0, x1 = x[2:].split('..')
        xrange = range(int(x0), int(x1)+1)
        y0, y1 = y[2:].split('..')
        yrange = range(int(y0), int(y1)+1)
        z0, z1 = z[2:].split('..')
        zrange = range(int(z0), int(z1)+1)

        yield state, xrange, yrange, zrange

def get_subrange(crange, low, high):
    c0 = crange[0]
    c1 = crange[-1]
    if c1 < low:
        return []
    elif c0 > high:
        return []
    c0 = max(c0, low)
    c1 = max(c1, low)
    c0 = min(c0, high)
    c1 = min(c1, high)
    return range(c0, c1+1)

def part1(s):
    data = list(parse_input(s))

    cubes = {}
    for idx, item in enumerate(data):
        state, xr, yr, zr = item
        for x in get_subrange(xr, -50, 50):
            for y in get_subrange(yr, -50, 50):
                for z in get_subrange(zr, -50, 50):
                    cubes[x,y,z] = state

    answer = sum(1 for s in cubes.values() if s == 'on')

    print(f'The answer to part one is {answer}')

def count_uninterrupted(item, rest):
    _, xr, yr, zr = item
    total = len(xr) * len(yr) * len(zr)

    conflicts = []
    ref_val = 0

    for item in rest:
        state, xr2, yr2, zr2 = item

        cxr = get_subrange(xr2, xr[0], xr[-1])
        cyr = get_subrange(yr2, yr[0], yr[-1])
        czr = get_subrange(zr2, zr[0], zr[-1])

        if len(cxr) == 0 or len(cyr) == 0 or len(czr) == 0:
            continue

        conflicts.append((state, cxr, cyr, czr))
        ref_val += len(cxr) * len(cyr) * len(czr)

    for idx, item in enumerate(conflicts):
        total -= count_uninterrupted(item, conflicts[idx+1:])

    return total

def part2(s):
    data = list(parse_input(s))

    answer = 0

    for idx, item in enumerate(data):
        state, xr, yr, zr = item
        if state == 'off':
            continue
        answer += count_uninterrupted(item, data[idx+1:])

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 22)
part1(INPUT)
part2(INPUT)
