import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(',')))

def part1(s):
    data = set(parse_input(s))

    answer = 0

    for x, y, z in data:
        for neighbor in [(x-1, y, z), (x+1, y, z),
                         (x, y-1, z), (x, y+1, z),
                         (x, y, z-1), (x, y, z+1)]:
            if neighbor not in data:
                answer += 1

    lib.aoc.give_answer(2022, 18, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 18)
part1(INPUT)
part2(INPUT)
