import lib.aoc

def part1(s):
    seen = {(0, 0)}

    x, y = 0, 0

    for c in s:
        if c == '>':
            x += 1
        elif c == '<':
            x -= 1
        elif c == '^':
            y -= 1
        elif c == 'v':
            y += 1
        else:
            assert(False)
        seen.add((x, y))

    answer = len(seen)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 3)
part1(INPUT)
part2(INPUT)
