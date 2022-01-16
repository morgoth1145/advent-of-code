import lib.aoc

def gen_coords():
    x, y = 0, 0
    dist = 1
    val = 1

    yield (x, y), val

    while True:
        for _ in range(dist):
            x += 1
            val += 1
            yield (x, y), val
        for _ in range(dist):
            y += 1
            val += 1
            yield (x, y), val
        dist += 1
        for _ in range(dist):
            x -= 1
            val += 1
            yield (x, y), val
        for _ in range(dist):
            y -= 1
            val += 1
            yield (x, y), val
        dist += 1

def part1(s):
    n = int(s)

    for (x, y), val in gen_coords():
        if val == n:
            answer = abs(x) + abs(y)
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    n = int(s)

    written = {
        (0, 0): 1
    }

    for (x, y), _ in gen_coords():
        val = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                val += written.get((x+dx, y+dy), 0)
        written[x, y] = val
        if val > n:
            answer = val
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 3)
part1(INPUT)
part2(INPUT)
