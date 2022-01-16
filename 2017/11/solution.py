import lib.aoc
import lib.hex_coord

def part1(s):
    pos = lib.hex_coord.NSHexCoord()

    for d in s.split(','):
        pos = pos.move(d)

    answer = pos.steps_from(lib.hex_coord.NSHexCoord())

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = 0
    pos = lib.hex_coord.NSHexCoord()

    for d in s.split(','):
        pos = pos.move(d)
        answer = max(answer, pos.steps_from(lib.hex_coord.NSHexCoord()))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 11)
part1(INPUT)
part2(INPUT)
