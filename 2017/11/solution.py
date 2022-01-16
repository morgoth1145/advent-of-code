import lib.aoc

def move(pos, d):
    a, b = pos

    if d == 'ne':
        a += 2
    elif d == 'n':
        a += 1
        b += 1
    elif d == 'nw':
        a -= 1
        b += 1
    elif d == 'sw':
        a -= 2
    elif d == 's':
        a -= 1
        b -= 1
    elif d == 'se':
        a += 1
        b -= 1
    else:
        assert(False)

    return a, b

def part1(s):
    pos = (0, 0)

    for d in s.split(','):
        pos = move(pos, d)
        assert(sum(map(abs, pos)) % 2 == 0)

    answer = sum(map(abs, pos)) // 2

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 11)
part1(INPUT)
part2(INPUT)
