import lib.aoc

def gen_coords():
    x, y = 0, 0
    dist = 1

    yield x, y

    while True:
        for _ in range(dist):
            x += 1
            yield x, y
        for _ in range(dist):
            y += 1
            yield x, y
        dist += 1
        for _ in range(dist):
            x -= 1
            yield x, y
        for _ in range(dist):
            y -= 1
            yield x, y
        dist += 1

def part1(s):
    n = int(s)

    for idx, (x, y) in enumerate(gen_coords()):
        if idx+1 == n:
            answer = abs(x) + abs(y)
            break

    lib.aoc.give_answer(2017, 3, 1, answer)

def part2(s):
    n = int(s)

    written = {
        (0, 0): 1
    }

    for x, y in gen_coords():
        val = sum(written.get((x+dx, y+dy), 0)
                  for dx in (-1, 0, 1)
                  for dy in (-1, 0, 1))
        written[x, y] = val
        if val > n:
            answer = val
            break

    lib.aoc.give_answer(2017, 3, 2, answer)

INPUT = lib.aoc.get_input(2017, 3)
part1(INPUT)
part2(INPUT)
