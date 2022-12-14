import lib.aoc

def parse_cave(s):
    cave = set()

    for line in s.splitlines():
        parts = [tuple(map(int, p.split(',')))
                 for p in line.split(' -> ')]
        x, y = parts.pop(0)
        for x2, y2 in parts:
            if x == x2:
                dy = -1 if y2 < y else 1
                cave.update((x, y) for y in range(y, y2+dy, dy))
                y = y2
            else:
                dx = -1 if x2 < x else 1
                cave.update((x, y) for x in range(x, x2+dx, dx))
                x = x2

    return cave

def solve(cave, in_x, in_y):
    max_y = max(y for x,y in cave)
    initial_count = len(cave)

    def settle(x, y):
        if y > max_y: # Part 1 exit condition
            return False
        if (x, y) in cave:
            return True
        # Will short circuit if any cannot settle
        if settle(x, y+1) and settle(x-1, y+1) and settle(x+1, y+1):
            cave.add((x, y))
            return True
        return False

    settle(in_x, in_y)

    return len(cave) - initial_count

def part1(s):
    answer = solve(parse_cave(s), 500, 0)
    lib.aoc.give_answer(2022, 14, 1, answer)

def part2(s):
    cave = parse_cave(s)

    # The sand can only go so far so we don't need an infinite floor
    floor = max(y for x,y in cave) + 2
    cave.update((x, floor) for x in range(500-floor, 500+floor+1))

    answer = solve(cave, 500, 0)
    lib.aoc.give_answer(2022, 14, 2, answer)

INPUT = lib.aoc.get_input(2022, 14)
part1(INPUT)
part2(INPUT)
