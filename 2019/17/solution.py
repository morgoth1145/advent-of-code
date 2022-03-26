import lib.aoc
import lib.grid

intcode = __import__('2019.intcode').intcode

def part1(s):
    _, out_chan = intcode.Program(s).run()

    grid = lib.grid.FixedGrid.parse(''.join(map(chr, out_chan)).strip())

    answer = 0

    for (x, y), c in grid.items():
        if c != '#':
            continue

        neighbors = list(grid.neighbors(x, y))
        if len(neighbors) != 4:
            continue

        if all(grid[n] == '#' for n in neighbors):
            answer += x*y

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 17)
part1(INPUT)
part2(INPUT)
