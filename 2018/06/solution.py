import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(',')))

def get_set_sizes(points, x_range, y_range):
    sizes = collections.Counter()

    for x in x_range:
        for y in y_range:
            best_dist = None
            cands = []
            for idx, (px, py) in enumerate(points):
                dist = abs(x-px) + abs(y-py)
                if best_dist is None or best_dist > dist:
                    best_dist = dist
                    cands = [idx]
                elif best_dist == dist:
                    cands.append(idx)
            if len(cands) == 1:
                sizes[cands[0]] += 1

    return sizes

def part1(s):
    points = list(parse_input(s))

    min_x = min(x for x,y in points)
    max_x = max(x for x,y in points)
    min_y = min(y for x,y in points)
    max_y = max(y for x,y in points)

    width = max_x-min_x+1
    height = max_y-min_y+1

    base_sizes = get_set_sizes(points,
                               range(min_x, max_x+1),
                               range(min_y, max_y+1))

    sizes = get_set_sizes(points,
                          range(min_x-width, max_x+1+width),
                          range(min_y-height, max_y+1+height))

    answer = 0
    for idx in range(len(points)):
        # Assume that a larger size means infinite
        # May not always be true
        if base_sizes[idx] == sizes[idx]:
            answer = max(answer, base_sizes[idx])

    print(f'The answer to part one is {answer}')

def part2(s):
    points = list(parse_input(s))

    min_x = min(x for x,y in points)
    max_x = max(x for x,y in points)
    min_y = min(y for x,y in points)
    max_y = max(y for x,y in points)

    width = max_x-min_x+1
    height = max_y-min_y+1

    answer = 0

    # The ranges are probably overkill
    for x in range(min_x-width, max_x+1+width):
        for y in range(min_y-height, max_y+1+height):
            tot_dist = 0
            for px, py in points:
                tot_dist += abs(x-px) + abs(y-py)
            if tot_dist < 10000:
                answer += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 6)
part1(INPUT)
part2(INPUT)
