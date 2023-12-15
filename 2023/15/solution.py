import lib.aoc

def the_hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256

    return v

def part1(s):
    bits = s.split(',')

    answer = sum(map(the_hash, bits))

    lib.aoc.give_answer(2023, 15, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 15)
part1(INPUT)
part2(INPUT)
