import lib.aoc

KEYS = {
    (0, 0): 1,
    (1, 0): 2,
    (2, 0): 3,
    (0, 1): 4,
    (1, 1): 5,
    (2, 1): 6,
    (0, 2): 7,
    (1, 2): 8,
    (2, 2): 9,
}

def interpret(directions):
    x, y = 1, 1

    for d in directions:
        if d == 'U':
            y = max(y-1, 0)
        elif d == 'D':
            y = min(y+1, 2)
        elif d == 'L':
            x = max(x-1, 0)
        elif d == 'R':
            x = min(x+1, 2)

    return str(KEYS[x,y])

def part1(s):
    answer = int(''.join(map(interpret, s.splitlines())))

    print(f'The answer to part one is {answer}')

INDICES = {
    (0, -2): 1,
    (-1, -1): 2,
    (0, -1): 3,
    (1, -1): 4,
    (-2, 0): 5,
    (-1, 0): 6,
    (0, 0): 7,
    (1, 0): 8,
    (2, 0): 9,
    (-1, 1): 10,
    (0, 1): 11,
    (1, 1): 12,
    (0, 2): 13,
}

def interpret2(directions):
    p = -2

    for d in directions:
        if d == 'U':
            np = p - 1j
        elif d == 'D':
            np = p + 1j
        elif d == 'L':
            np = p - 1
        elif d == 'R':
            np = p + 1

        man_dist = int(abs(np.real) + abs(np.imag))
        if man_dist <= 2:
            p = np

    return '123456789ABCD'[INDICES[int(p.real), int(p.imag)]-1]

def part2(s):
    answer = ''.join(map(interpret2, s.splitlines()))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 2)
part1(INPUT)
part2(INPUT)
