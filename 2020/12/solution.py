import lib.aoc

def part1(s):
    dx, dy = 1, 0
    x = 0
    y = 0
    for act in s.splitlines():
        t = act[0]
        n = int(act[1:])
        if t == 'N':
            y += n
        if t == 'S':
            y -= n
        if t == 'E':
            x += n
        if t == 'W':
            x -= n
        if t == 'L':
            for _ in range(n//90):
                dx, dy = -dy, dx
        if t == 'R':
            for _ in range(n//90):
                dx, dy = dy, -dx
        if t == 'F':
            x += dx*n
            y += dy*n
    answer = abs(x) + abs(y)
    print(f'The answer to part one is {answer}')

def part2(s):
    sx, sy = 0, 0
    x = 10
    y = 1
    for act in s.splitlines():
        t = act[0]
        n = int(act[1:])
        if t == 'N':
            y += n
        if t == 'S':
            y -= n
        if t == 'E':
            x += n
        if t == 'W':
            x -= n
        if t == 'L':
            for _ in range(n//90):
                x, y = -y, x
        if t == 'R':
            for _ in range(n//90):
                x, y = y, -x
        if t == 'F':
            sx += x*n
            sy += y*n
    answer = abs(sx) + abs(sy)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2020, 12)

part1(INPUT)
part2(INPUT)
