import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield line.split()

def part1(s):
    answer = 0

    for passphrase in parse_input(s):
        if len(passphrase) == len(set(passphrase)):
            answer += 1

    lib.aoc.give_answer(2017, 4, 1, answer)

def part2(s):
    answer = 0

    for passphrase in parse_input(s):
        passphrase = [tuple(sorted(part))
                      for part in passphrase]
        if len(passphrase) == len(set(passphrase)):
            answer += 1

    lib.aoc.give_answer(2017, 4, 2, answer)

INPUT = lib.aoc.get_input(2017, 4)
part1(INPUT)
part2(INPUT)
