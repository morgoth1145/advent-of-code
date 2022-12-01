import lib.aoc

def parse_input(s):
    for elf in s.split('\n\n'):
        yield sum(map(int, elf.splitlines()))

def part1(s):
    answer = max(parse_input(s))

    lib.aoc.give_answer(2022, 1, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 1)
part1(INPUT)
part2(INPUT)
