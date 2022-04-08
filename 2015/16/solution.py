import lib.aoc

def find_match(s, *checks):
    for line in s.splitlines():
        _, n, a, ac, b, bc, c, cc = line.split()

        num, info = line.split(': ', maxsplit=1)

        things = {}
        for thing in info.split(', '):
            name, count = thing.split(': ')
            things[name] = int(count)

        if all(check(things)
               for check in checks):
            return int(num.split()[1])

EXPECTED_EQ = [('children', 3),
               ('samoyeds', 2),
               ('akitas', 0),
               ('vizslas', 0),
               ('cars', 2),
               ('perfumes', 1)]
EXPECTED_GT = [('cats', 7),
               ('trees', 3)]
EXPECTED_LT = [('pomeranians', 3),
               ('goldfish', 5)]

def make_eq_check(expectations):
    def impl(things):
        return all(things.get(key, expected) == expected
                   for key, expected in expectations)
    return impl

def part1(s):
    answer = find_match(s,
                        make_eq_check(EXPECTED_EQ + EXPECTED_GT + EXPECTED_LT))

    lib.aoc.give_answer(2015, 16, 1, answer)

def make_gt_check(expectations):
    def impl(things):
        return all(things.get(key, expected+1) > expected
                   for key, expected in expectations)
    return impl

def make_lt_check(expectations):
    def impl(things):
        return all(things.get(key, expected-1) < expected
                   for key, expected in expectations)
    return impl

def part2(s):
    answer = find_match(s,
                        make_eq_check(EXPECTED_EQ),
                        make_gt_check(EXPECTED_GT),
                        make_lt_check(EXPECTED_LT))

    lib.aoc.give_answer(2015, 16, 2, answer)

INPUT = lib.aoc.get_input(2015, 16)
part1(INPUT)
part2(INPUT)
