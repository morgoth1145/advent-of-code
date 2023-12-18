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
    pass

INPUT = lib.aoc.get_input(2023, 18)
part1(INPUT)
part2(INPUT)
