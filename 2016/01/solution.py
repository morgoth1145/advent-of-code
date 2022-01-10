import lib.aoc

def walk_directions(s):
    d = 1j
    p = 0

    for move in s.split(', '):
        if move[0] == 'R':
            d *= -1j
        else:
            d *= 1j

        for _ in range(int(move[1:])):
            p += d
            yield p

def part1(s):
    p = list(walk_directions(s))[-1]

    answer = int(abs(p.real) + abs(p.imag))

    print(f'The answer to part one is {answer}')

def part2(s):
    seen = {0}

    for p in walk_directions(s):
        if p in seen:
            break
        seen.add(p)

    answer = int(abs(p.real) + abs(p.imag))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 1)
part1(INPUT)
part2(INPUT)
