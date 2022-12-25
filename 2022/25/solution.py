import lib.aoc

def translate_num(num):
    place = 1
    total = 0
    for c in num[::-1]:
        if c == '-':
            c = -1
        elif c == '=':
            c = -2
        else:
            c = int(c)
        total += c * place
        place *= 5

    return total

def to_snafu(num):
    places = [1]
    while places[0] < num:
        places.insert(0, 5 * places[0])

    def impl(n, places):
        if len(places) == 0:
            if n == 0:
                return ''
            else:
                return None

        if places[0] * 3 < n:
            return None

        if places[0] * -3 > n:
            return None

        for mult, c in zip((2, 1, 0, -1, -2), '210-='):
            res = impl(n - mult * places[0], places[1:])
            if res is not None:
                return c + res

        return None

    return impl(num, places).lstrip('0')

def part1(s):
    answer = to_snafu(sum(map(translate_num, s.splitlines())))

    lib.aoc.give_answer(2022, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2022, 25)
part1(INPUT)
part2(INPUT)
