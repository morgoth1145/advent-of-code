import helpers.input

def part1(s):
    dx, dy = 1, 0
    x = 0
    y = 0
    for act in s.splitlines():
        t = act[0]
        n = int(act[1:])
        if t == 'N':
            y += n
            continue
        if t == 'S':
            y -= n
            continue
        if t == 'E':
            x += n
            continue
        if t == 'W':
            x -= n
            continue
        if t == 'L':
            for _ in range(n//90):
                dx, dy = -dy, dx
            continue
        if t == 'R':
            for _ in range(n//90):
                dx, dy = dy, -dx
            continue
        if t == 'F':
            x += dx*n
            y += dy*n
            continue
    answer = abs(x) + abs(y)
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 12)

part1(INPUT)
part2(INPUT)
