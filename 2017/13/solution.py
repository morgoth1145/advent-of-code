import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield tuple(map(int, line.split(':')))

def part1(s):
    answer = 0

    for depth, layers in parse_input(s):
        cycle = 2 * (layers - 1)
        if cycle == 0:
            cycle = 1
        if depth % cycle == 0:
            # Caught!
            answer += depth * layers

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 13)
part1(INPUT)
part2(INPUT)
