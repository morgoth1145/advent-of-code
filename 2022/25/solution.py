import lib.aoc

def parse_snafu(num):
    total = 0
    for c in num:
        total = total * 5 + ('=-012'.index(c) - 2)

    return total

def to_snafu(num):
    output = ''

    while num != 0:
        # Offsetting the number at this place makes conversion simple
        num, place = divmod(num + 2, 5)
        output += '=-012'[place]

    return output[::-1]

def part1(s):
    answer = to_snafu(sum(map(parse_snafu, s.splitlines())))

    lib.aoc.give_answer(2022, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2022, 25)
part1(INPUT)
part2(INPUT)
