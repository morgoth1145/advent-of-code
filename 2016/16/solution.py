import lib.aoc

def solve(s, disk):
    # Expand
    while len(s) < disk:
        s = s + '0' + s[::-1].translate(str.maketrans('01', '10'))

    s = s[:disk]

    # Checksum
    while len(s) % 2 == 0:
        s = ''.join('1' if a == b else '0'
                    for a, b in zip(s[::2], s[1::2]))

    return s

def part1(s):
    answer = solve(s, 272)

    lib.aoc.give_answer(2016, 16, 1, answer)

def part2(s):
    answer = solve(s, 35651584)

    lib.aoc.give_answer(2016, 16, 2, answer)

INPUT = lib.aoc.get_input(2016, 16)
part1(INPUT)
part2(INPUT)
