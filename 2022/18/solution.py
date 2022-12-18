import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(',')))

def neighbors(x, y, z):
    return [(x-1, y, z), (x+1, y, z),
            (x, y-1, z), (x, y+1, z),
            (x, y, z-1), (x, y, z+1)]

def part1(s):
    data = set(parse_input(s))

    answer = 0

    for x, y, z in data:
        for n in neighbors(x, y, z):
            if n not in data:
                answer += 1

    lib.aoc.give_answer(2022, 18, 1, answer)

def part2(s):
    data = set(parse_input(s))

    min_x = min(x for x,y,z in data)
    max_x = max(x for x,y,z in data)
    min_y = min(y for x,y,z in data)
    max_y = max(y for x,y,z in data)
    min_z = min(z for x,y,z in data)
    max_z = max(z for x,y,z in data)

    x_range = range(min_x, max_x+1)
    y_range = range(min_y, max_y+1)
    z_range = range(min_z, max_z+1)

    known_exterior = set()

    def is_exterior(x, y, z):
        if (x, y, z) in data:
            return False

        checked = set()
        todo = [(x, y, z)]

        while todo:
            x, y, z = todo.pop()
            if (x, y, z) in checked:
                continue
            checked.add((x, y, z))
            if (x, y, z) in known_exterior:
                known_exterior.update(checked - data)
                return True
            if x not in x_range or y not in y_range or z not in z_range:
                # We breached the range, it's exterior!
                known_exterior.update(checked - data)
                return True
            if (x, y, z) not in data:
                todo += neighbors(x, y, z)

        # We couldn't reach the outside!
        return False

    answer = 0

    for x, y, z in data:
        for n in neighbors(x, y, z):
            if is_exterior(*n):
                answer += 1

    lib.aoc.give_answer(2022, 18, 2, answer)

INPUT = lib.aoc.get_input(2022, 18)
part1(INPUT)
part2(INPUT)
