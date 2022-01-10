import lib.aoc

def count_possible_triangles(tris):
    count = 0

    for a, b, c in tris:
        maxlen = max(a, b, c)
        if a+b+c - maxlen > maxlen:
            count += 1

    return count

def part1(s):
    tris = [list(map(int, line.split()))
            for line in s.splitlines()]

    answer = count_possible_triangles(tris)

    print(f'The answer to part one is {answer}')

def column_tris(s):
    lines = s.splitlines()
    while lines:
        a = lines.pop(0).split()
        b = lines.pop(0).split()
        c = lines.pop(0).split()

        yield int(a.pop(0)), int(b.pop(0)), int(c.pop(0))
        yield int(a.pop(0)), int(b.pop(0)), int(c.pop(0))
        yield int(a.pop(0)), int(b.pop(0)), int(c.pop(0))

def part2(s):
    answer = count_possible_triangles(column_tris(s))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 3)
part1(INPUT)
part2(INPUT)
