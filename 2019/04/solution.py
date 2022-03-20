import lib.aoc

def valid_password(p):
    p = str(p)

    if len(p) != 6:
        return False

    doubled = False
    for a, b in zip(p, p[1:]):
        if a == b:
            doubled = True
            continue

        if int(a) > int(b):
            return False

    return doubled

def part1(s):
    a, b = list(map(int, s.split('-')))

    answer = sum(map(valid_password, range(a, b+1)))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 4)
part1(INPUT)
part2(INPUT)
