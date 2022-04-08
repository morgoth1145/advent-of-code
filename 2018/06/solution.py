import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(',')))

def closest_point(points, x, y):
    best_dist = None
    cands = []
    for idx, (px, py) in enumerate(points):
        dist = abs(x-px) + abs(y-py)
        if best_dist is None or best_dist > dist:
            best_dist = dist
            cands = [idx]
        elif best_dist == dist:
            cands.append(idx)

    # If there's a conflict, nothing is closest
    if len(cands) > 1:
        return None
    return cands[0]

def part1(s):
    points = list(parse_input(s))

    min_x = min(x for x,y in points)
    max_x = max(x for x,y in points)
    min_y = min(y for x,y in points)
    max_y = max(y for x,y in points)

    x_range = range(min_x, max_x+1)
    y_range = range(min_y, max_y+1)

    sizes = collections.Counter()

    for x in x_range:
        for y in y_range:
            sizes[closest_point(points, x, y)] += 1

    infinites = set()

    for x in x_range:
        infinites.add(closest_point(points, x, min_y))
        infinites.add(closest_point(points, x, max_y))
    for y in y_range:
        infinites.add(closest_point(points, min_x, y))
        infinites.add(closest_point(points, max_x, y))

    answer = max(count
                 for best, count in sizes.items()
                 if best is not None
                 if best not in infinites)

    lib.aoc.give_answer(2018, 6, 1, answer)

def part2(s):
    points = list(parse_input(s))

    mid_x = sum(x for x,y in points) // len(points)
    mid_y = sum(y for x,y in points) // len(points)

    seen = {(mid_x, mid_y)}
    to_check = [(mid_x, mid_y)]
    answer = 0

    while to_check:
        x, y = to_check.pop(-1)

        tot_dist = sum(abs(x-px) + abs(y-py)
                       for px, py in points)

        if tot_dist >= 10000:
            continue

        answer += 1

        for neighbor in [(x-1, y),
                         (x+1, y),
                         (x, y-1),
                         (x, y+1)]:
            if neighbor in seen:
                continue
            to_check.append(neighbor)
            seen.add(neighbor)

    lib.aoc.give_answer(2018, 6, 2, answer)

INPUT = lib.aoc.get_input(2018, 6)
part1(INPUT)
part2(INPUT)
