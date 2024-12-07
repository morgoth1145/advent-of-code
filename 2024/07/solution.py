import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        target, rest = line.split(':')
        yield int(target), tuple(map(int, rest.split()))

def is_solvable(target, parts):
    def impl(current, rest):
        if len(rest) == 0:
            if current == target:
                return True
            return False

        a = rest[0]
        rest = rest[1:]

        if impl(current+a, rest):
            return True
        if impl(current*a, rest):
            return True
        return False

    return impl(parts[0], parts[1:])

def part1(s):
    data = parse_input(s)

    answer = 0

    for target, parts in data:
        if is_solvable(target, parts):
            answer += target

    lib.aoc.give_answer(2024, 7, 1, answer)

def is_solvable2(target, parts):
    def impl(current, rest):
        if len(rest) == 0:
            if current == target:
                return True
            return False

        a = rest[0]
        rest = rest[1:]

        if impl(current+a, rest):
            return True
        if impl(current*a, rest):
            return True
        if impl(int(str(current)+str(a)), rest):
            return True
        return False

    return impl(parts[0], parts[1:])

def part2(s):
    data = parse_input(s)

    answer = 0

    for target, parts in data:
        if is_solvable2(target, parts):
            answer += target

    lib.aoc.give_answer(2024, 7, 2, answer)

INPUT = lib.aoc.get_input(2024, 7)
part1(INPUT)
part2(INPUT)
