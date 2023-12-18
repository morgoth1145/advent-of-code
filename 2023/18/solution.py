import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b, c = line.split()
        b = int(b)
        c = int(c[2:-1], base=16)
        yield a, b, c

def part1(s):
    data = list(parse_input(s))

    x, y = 0, 0

    seen = set()
    seen.add((x, y))

    for d, num, _ in data:
        if d == 'U':
            dx, dy = 0, -1
        elif d == 'D':
            dx, dy = 0, 1
        elif d == 'R':
            dx, dy = 1, 0
        else:
            dx, dy = -1, 0

        for _ in range(num):
            x, y = x+dx, y+dy
            seen.add((x, y))

    min_x = min(x for x,y in seen)
    max_x = max(x for x,y in seen)
    min_y = min(y for x,y in seen)
    max_y = max(y for x,y in seen)

    x_range = range(min_x, max_x+1)
    y_range = range(min_y, max_y+1)

    fill = set(seen)

    for y in y_range:
        is_enclosed = False
        for x in x_range:
            if (x,y) in seen:
                if (x, y-1) in seen and (x, y+1) in seen:
                    is_enclosed = not is_enclosed
                elif (x,y+1) in seen and (x+1,y) in seen:
                    is_enclosed = not is_enclosed
                elif (x,y+1) in seen and (x-1,y) in seen:
                    is_enclosed = not is_enclosed
            else:
                if is_enclosed:
                    fill.add((x,y))

    answer = len(fill)

    lib.aoc.give_answer(2023, 18, 1, answer)

def part2(s):
    data = list(parse_input(s))

    x, y = 0, 0

    corners = [(x,y)]

    x_points = set()
    y_points = set()

    for _, _, num in data:
        d = 'RDLU'[num&0xF]
        num //= 16
        if d == 'U':
            dx, dy = 0, -1
        elif d == 'D':
            dx, dy = 0, 1
        elif d == 'R':
            dx, dy = 1, 0
        else:
            dx, dy = -1, 0

        x += dx*num
        y += dy*num
        corners.append((x,y))
        x_points.add(x)
        y_points.add(y)

    x_points = sorted(x_points)
    y_points = sorted(y_points)

    compression = {}

    grid_sizes = {}

    new_x = 0

    for ix, x in enumerate(x_points):
        new_y = 0
        for iy, y in enumerate(y_points):
            compression[x,y] = (new_x, new_y)

            grid_sizes[new_x,new_y] = 1

            if ix > 0:
                last_x = x_points[ix-1]
                grid_sizes[new_x-1,new_y] = (x-last_x-1)
                if iy > 0:
                    last_y = y_points[iy-1]
                    grid_sizes[new_x-1,new_y-1] = (x-last_x-1) * (y-last_y-1)
            if iy > 0:
                last_y = y_points[iy-1]
                grid_sizes[new_x,new_y-1] = (y-last_y-1)

            new_y += 2

        new_x += 2

    seen = set()

    for (e0, e1) in zip(corners, corners[1:] + [corners[0]]):
        x0, y0 = compression[e0]
        x1, y1 = compression[e1]

        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                seen.add((x,y))

    min_x = min(x for x,y in seen)
    max_x = max(x for x,y in seen)
    min_y = min(y for x,y in seen)
    max_y = max(y for x,y in seen)

    x_range = range(min_x, max_x+1)
    y_range = range(min_y, max_y+1)

    fill = set(seen)

    for y in y_range:
        is_enclosed = False
        for x in x_range:
            if (x,y) in seen:
                if (x, y-1) in seen and (x, y+1) in seen:
                    is_enclosed = not is_enclosed
                elif (x,y+1) in seen and (x+1,y) in seen:
                    is_enclosed = not is_enclosed
                elif (x,y+1) in seen and (x-1,y) in seen:
                    is_enclosed = not is_enclosed
            else:
                if is_enclosed:
                    fill.add((x,y))

    answer = sum(map(grid_sizes.__getitem__,
                     fill))

    lib.aoc.give_answer(2023, 18, 2, answer)

INPUT = lib.aoc.get_input(2023, 18)
part1(INPUT)
part2(INPUT)
