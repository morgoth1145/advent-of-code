import lib.aoc

def parse_cave(s):
    cave = {}

    for line in s.splitlines():
        parts = line.split(' -> ')
        parts = [tuple(map(int, p.split(',')))
                 for p in parts]
        x, y = parts.pop(0)
        cave[x,y] = '#'
        for x2, y2 in parts:
            dx, dy = x2-x, y2-y
            if dx != 0:
                dx = dx // abs(dx)
            if dy != 0:
                dy = dy // abs(dy)

            while x != x2 or y != y2:
                x += dx
                y += dy
                cave[x,y] = '#'

    return cave

def generate_sand(cave, in_x, in_y, max_y):
    x = in_x
    y = in_y
    while (x,y) not in cave:
        if y > max_y:
            return False
        if (x,y+1) not in cave:
            y += 1
            continue
        if (x-1,y+1) not in cave:
            x -= 1
            y += 1
            continue
        if (x+1,y+1) not in cave:
            x += 1
            y += 1
            continue
        # This must have settled
        cave[x,y] = 'o'
        return True

def part1(s):
    cave = parse_cave(s)

    max_y = max(y for x,y in cave.keys())

    answer = 0

    while generate_sand(cave, 500, 0, max_y):
        answer += 1

    lib.aoc.give_answer(2022, 14, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 14)
part1(INPUT)
part2(INPUT)
