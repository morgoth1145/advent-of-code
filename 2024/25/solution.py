import lib.aoc
import lib.grid

def parse_input(s):
    locks = []
    keys = []

    for group in s.split('\n\n'):
        grid = lib.grid.FixedGrid.parse(group)
        if grid[0,0] == '#':
            locks.append(grid)
        else:
            keys.append(grid)

    return locks, keys

def part1(s):
    locks, keys = parse_input(s)

    answer = 0

    for l in locks:
        for k in keys:
            good = True
            for coord, c in l.items():
                kc = k[coord]
                if c == '#' == kc:
                    good = False
                    break
            if good:
                answer += 1

    lib.aoc.give_answer(2024, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2024, 25)
part1(INPUT)
part2(INPUT)
