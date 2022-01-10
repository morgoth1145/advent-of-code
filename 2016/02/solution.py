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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 2)
part1(INPUT)
part2(INPUT)
