import lib.aoc

def part1(s):
    d = 1j
    p = 0

    for move in s.split(', '):
        t = move[0]
        dist = int(move[1:])
        if t == 'R':
            d *= -1j
        else:
            d *= 1j
        p += dist * d

    answer = int(abs(p.real) + abs(p.imag))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 1)
part1(INPUT)
part2(INPUT)