import lib.aoc

def part1(s):
    pairs = [tuple(map(int, l.split(',')))
             for l in s.splitlines()]

    answer = 0

    for idx, (x, y) in enumerate(pairs):
        for x2, y2 in pairs[idx+1:]:
            area = (abs(x-x2)+1) * (abs(y-y2)+1)
            answer = max(answer, area)

    lib.aoc.give_answer(2025, 9, 1, answer)

def part2(s):
    vertices = [tuple(map(int, l.split(',')))
                for l in s.splitlines()]

    valid_x_vals = sorted(set(x for x,y in vertices))
    valid_y_vals = sorted(set(y for x,y in vertices))

    x_map = {}
    x_back_map = {}

    last_x = None
    next_x = 0

    for x in valid_x_vals:
        if last_x is not None:
            x_back_map[next_x] = x - last_x - 1
            next_x += 1
        x_map[x] = next_x
        x_back_map[next_x] = 1
        next_x += 1
        last_x = x

    y_map = {}
    y_back_map = {}

    last_y = None
    next_y = 0

    for y in valid_y_vals:
        if last_y is not None:
            y_back_map[next_y] = y - last_y - 1
            next_y += 1
        y_map[y] = next_y
        y_back_map[next_y] = 1
        next_y += 1
        last_y = y

    vertices = [(x_map[x], y_map[y])
                for x,y in vertices]

    vert_edges = []

    valid_tiles = set()

    for (x, y), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1]):
        if x == x2:
            edge_dir = (y < y2)
            vert_edges.append((x, min(y, y2), max(y, y2), edge_dir))
        else:
            assert(y == y2)
            for x3 in range(min(x, x2), max(x, x2)+1):
                # Add tiles on horizontal edges
                # the below code doesn't handle them right sometimes
                valid_tiles.add((x3, y))

    minx = min(x for x,y in vertices)
    maxx = max(x for x,y in vertices)

    miny = min(y for x,y in vertices)
    maxy = max(y for x,y in vertices)

    for y in range(miny, maxy+1):
        included = False
        last_edge_dir = None
        for x in range(minx, maxx+1):
            hit_edge = False
            for edgex, edgey, edgey2, edge_dir in vert_edges:
                if x == edgex and edgey <= y <= edgey2:
                    if edge_dir != last_edge_dir:
                        hit_edge = True
                        last_edge_dir = edge_dir
                        break

            if hit_edge:
                # We hit an edge
                valid_tiles.add((x,y))
                included = not included
                continue

            if included:
                valid_tiles.add((x,y))

    candidates = []

    def make_area_set(c, c2):
        x, y = c
        x2, y2 = c2
        if x > x2:
            x, x2 = x2, x
        if y > y2:
            y, y2 = y2, y
        return set((x3, y3)
                   for x3 in range(x, x2+1)
                   for y3 in range(y, y2+1))

    def calc_area(area_set):
        area = 0

        for x,y in area_set:
            area += x_back_map[x] * y_back_map[y]

        return area

    for idx, (x, y) in enumerate(vertices):
        for x2, y2 in vertices[idx+1:]:
            candidates.append(((x, y), (x2, y2)))

    candidates.sort(reverse=True)

    answer = 0

    for idx, (c, c2) in enumerate(candidates):
        valid = True
        
        x, y = c
        x2, y2 = c2
        if x > x2:
            x, x2 = x2, x
        if y > y2:
            y, y2 = y2, y

        for x3, y3 in vertices:
            if x < x3 < x2:
                if y < y3 < y2:
                    valid = False
                    break

        if valid:
            area_set = make_area_set(c, c2)
            if len(area_set) == len(area_set & valid_tiles):
                area2 = calc_area(area_set)
                answer = max(answer, area2)

    lib.aoc.give_answer(2025, 9, 2, answer)

INPUT = lib.aoc.get_input(2025, 9)
part1(INPUT)
part2(INPUT)
