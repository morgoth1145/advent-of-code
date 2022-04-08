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

    lib.aoc.give_answer(2019, 4, 1, answer)

def valid_password2(p):
    p = list(map(int, str(p)))

    if len(p) != 6:
        return False

    double = False
    last = p[0]
    last_start = 0
    for idx, d in enumerate(p[1:]):
        idx += 1

        if d < last:
            return False
        if d > last:
            if idx - last_start == 2:
                double = True
            last = d
            last_start = idx

    if len(p) - last_start == 2:
        double = True

    return double

def part2(s):
    a, b = list(map(int, s.split('-')))

    answer = sum(map(valid_password2, range(a, b+1)))

    lib.aoc.give_answer(2019, 4, 2, answer)

INPUT = lib.aoc.get_input(2019, 4)
part1(INPUT)
part2(INPUT)
